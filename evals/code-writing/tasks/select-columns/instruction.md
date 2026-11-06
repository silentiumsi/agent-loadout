Add selectable CSV columns to the order exporter in `/app/project`.

`python -m orders.export orders.json --columns 'email,id'` must write those
canonical headers in that order and the corresponding values. Omission keeps
the current `id,email,total,note` output, including its CSV escaping and empty
input header. Existing callers of `render_csv(rows)` must keep working.

Column selection follows the same user-facing convention as the table command:
a single CSV record, case-insensitive names, surrounding whitespace ignored,
aliases resolved, and duplicates removed after resolution while keeping the
first occurrence. The aliases documented in README.md apply to both commands.
Reject empty selections, empty items, unknown names, malformed CSV, and multiple
records with argparse-style exit 2, a useful error on stderr, and no stdout.
Validate the selection before reading the input file. Preserve current valid
exports and table behavior.

Add regression tests using the project's unittest command. Test what users can
observe, including a selected export and an invalid selection. Do not add
dependencies. Keep the existing sample data and tests intact. Finish with a brief account of the change and checks run.
