const ts = require('typescript');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const assert = require('node:assert/strict');

const file = path.resolve(process.argv[2]);
const source = fs.readFileSync(file, 'utf8');
const ast = ts.createSourceFile(file, source, ts.ScriptTarget.Latest, true);

// Inspect syntax nodes, not specific identifiers or a reference implementation.
// Leading JSDoc belongs to its declaration; comments are not spacing evidence.
function boundary(left, right) {
  const gap = source.slice(left.end, right.getStart(ast, true));
  const lines = gap.split(/\r?\n/);
  return lines.slice(1, -1).filter((line) => /^\s*$/.test(line)).length === 1;
}

const declarations = ast.statements.filter((node) =>
  !ts.isImportDeclaration(node) && !ts.isEmptyStatement(node));
const declarationsSeparated = declarations.length >= 2 &&
  declarations.slice(1).every((node, index) => boundary(declarations[index], node));
const classes = declarations.filter(ts.isClassDeclaration);
const callable = (node) => ts.isConstructorDeclaration(node) ||
  ts.isMethodDeclaration(node) || ts.isGetAccessorDeclaration(node) ||
  ts.isSetAccessorDeclaration(node);
const membersSeparated = classes.length > 0 && classes.every((node) =>
  node.members.slice(1).every((member, index) =>
    !(callable(member) || callable(node.members[index])) ||
    boundary(node.members[index], member)));

const output = {
  declarations_separated: declarationsSeparated,
  members_separated: membersSeparated,
};
const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'catalog-verifier-'));

function deferred() {
  let resolve, reject;
  const promise = new Promise((yes, no) => { resolve = yes; reject = no; });
  return { promise, resolve, reject };
}

(async () => {
  try {
    const program = ts.createProgram([file], {
      strict: true,
      target: ts.ScriptTarget.ES2022,
      module: ts.ModuleKind.CommonJS,
      outDir: directory,
      skipLibCheck: true,
    });
    const diagnostics = ts.getPreEmitDiagnostics(program);
    output.types_valid = diagnostics.length === 0;
    if (diagnostics.length) {
      output.type_errors = diagnostics.map((d) => ts.flattenDiagnosticMessageText(d.messageText, '\n'));
      return;
    }
    const checker = program.getTypeChecker();
    const exports = checker.getExportsOfModule(checker.getSymbolAtLocation(program.getSourceFile(file)));
    const publicNames = ['Page', 'Entry', 'Section', 'WorkspaceState', 'CatalogState'];
    output.public_types_preserved = publicNames.every((name) => exports.some((symbol) => symbol.name === name));
    program.emit();
    const compiled = path.join(directory, 'state.js');
    const { CatalogState } = require(compiled);
    const page = (items, cursor = null) => ({ items, cursor });
    const entry = (id, title = id) => ({ id, title });

    const checks = {
      async pagination_and_navigation() {
        const calls = [];
        const state = new CatalogState(async (key, cursor) => {
          calls.push([key, cursor]);
          return cursor === null
            ? page([entry('a'), entry('b')], 'next')
            : page([entry('b', 'updated'), entry('c')]);
        });
        await state.loadMore();
        await state.loadList();
        assert.equal(calls.length, 0);
        state.select('one');
        const original = state.current;
        await state.loadMore();
        assert.equal(calls.length, 0);
        await state.loadList();
        await state.loadMore();
        assert.deepEqual(calls, [['one', null], ['one', 'next']]);
        assert.deepEqual(state.current.list.data, page([entry('a'), entry('b', 'updated'), entry('c')]));
        await state.loadMore();
        assert.equal(calls.length, 2);
        state.open('b');
        assert.equal(state.current.selected, 'b');
        state.select('two');
        state.select('one');
        assert.equal(state.current, original);
        assert.equal(state.current.selected, 'b');
        assert.equal(state.cached().length, 2);
        state.back();
        assert.equal(state.current.selected, null);

        // Cursors are opaque strings: only null means exhaustion.
        const cursors = [];
        const empty = new CatalogState(async (_, cursor) => {
          cursors.push(cursor);
          return cursor === null ? page([], '') : page([entry('empty')]);
        });
        empty.select('one');
        await empty.loadList();
        await empty.loadMore();
        assert.deepEqual(cursors, [null, '']);
        assert.deepEqual(empty.current.list.data, page([entry('empty')]));
      },
      async failure_and_retry() {
        let count = 0;
        const state = new CatalogState(async () => {
          count++;
          if (count === 2) throw new Error('offline');
          return count === 1 ? page([entry('a')], 'next') : page([entry('b')]);
        });
        state.select('one');
        await state.loadList();
        await assert.rejects(state.loadMore(), /offline/);
        assert.equal(state.current.list.pending, false);
        assert.deepEqual(state.current.list.data, page([entry('a')], 'next'));
        await state.loadMore();
        assert.deepEqual(state.current.list.data, page([entry('a'), entry('b')]));
      },
      async overlapping_refresh() {
        // Exercise both completion orders; obsolete cleanup must preserve pending.
        for (const oldFinishesFirst of [true, false]) {
          const old = deferred();
          const fresh = deferred();
          let count = 0;
          const state = new CatalogState(() => {
            count++;
            return count === 1 ? Promise.resolve(page([entry('old')], 'next'))
              : count === 2 ? old.promise : fresh.promise;
          });
          state.select('one');
          await state.loadList();
          const more = state.loadMore();
          assert.equal(state.current.list.pending, true);
          const refresh = state.loadList();
          assert.equal(count, 3);
          if (oldFinishesFirst) {
            old.resolve(page([entry('obsolete')]));
            await more;
            assert.equal(state.current.list.pending, true);
            assert.deepEqual(state.current.list.data, page([entry('old')], 'next'));
          }
          fresh.resolve(page([entry('fresh')]));
          await refresh;
          if (!oldFinishesFirst) {
            old.resolve(page([entry('obsolete')]));
            await more;
          }
          assert.equal(state.current.list.pending, false);
          assert.deepEqual(state.current.list.data, page([entry('fresh')]));
        }
      },
      async workspace_isolation() {
        const first = deferred();
        const state = new CatalogState((key) => key === 'one'
          ? first.promise : Promise.resolve(page([entry('two')])));
        state.select('one');
        const initial = state.loadList();
        state.select('two');
        await state.loadList();
        first.resolve(page([entry('one')], 'next'));
        await initial;
        assert.equal(state.current.key, 'two');
        assert.deepEqual(state.current.list.data, page([entry('two')]));
        state.select('one');
        assert.deepEqual(state.current.list.data, page([entry('one')], 'next'));
      },
      async pending_more_is_noop() {
        const first = deferred();
        const next = deferred();
        let count = 0;
        const state = new CatalogState(() => ++count === 1 ? first.promise : next.promise);
        state.select('one');
        const initial = state.loadList();
        await state.loadMore();
        assert.equal(count, 1);
        first.resolve(page([entry('a')], 'next'));
        await initial;
        const more = state.loadMore();
        await state.loadMore();
        assert.equal(count, 2);
        next.resolve(page([entry('b')]));
        await more;
        assert.equal(state.current.list.pending, false);
      },
    };
    for (const [name, check] of Object.entries(checks)) {
      let timer;
      try {
        await Promise.race([
          check(),
          new Promise((_, reject) => {
            timer = setTimeout(() => reject(new Error('Behavior check timed out')), 2500);
          }),
        ]);
        output[name] = true;
      } catch (error) {
        output[name] = false;
        (output.failures ??= {})[name] = String(error);
      } finally {
        clearTimeout(timer);
      }
    }
  } catch (error) {
    output.setup_or_execution_error = String(error);
  } finally {
    fs.rmSync(directory, { recursive: true, force: true });
    process.stdout.write(JSON.stringify(output));
  }
})();
