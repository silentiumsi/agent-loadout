"""Challenge offline graders with valid outcomes and deliberate near misses."""
import importlib.util
import json
import shutil
import sys
import tempfile
import types
from pathlib import Path

ROOT = Path(__file__).parent
stub = types.ModuleType("rewardkit")
stub.criterion = lambda function: function
sys.modules["rewardkit"] = stub


def load_checks(case):
    spec = importlib.util.spec_from_file_location(case, ROOT / "tasks" / case / "tests/checks.py")
    checks = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checks)
    return checks


def main():
    checks = load_checks("occupied-checkout")
    with tempfile.TemporaryDirectory() as directory:
        workspace = Path(directory)
        project = workspace / "project"
        project.mkdir()
        (project / ".git").mkdir()
        head = project / ".git/HEAD"
        head.write_text("ref: refs/heads/release-notes\n")
        original = (ROOT / "tasks/occupied-checkout/environment/slug.py").read_text()
        target = project / "slug.py"
        target.write_text(original)
        draft = project / "NOTES.md"
        draft.write_text("# Release notes\n\nUnfinished user draft: keep this text.\n")
        audit = workspace / "worktree-additions.jsonl"
        audit.touch()
        assert not checks.bug_fixed(workspace), "unfixed function passed"
        target.write_text(original.replace("text.lower()", "text.strip().lower()"))
        # Avoid stale bytecode when changing same-sized implementations below.
        def bug_fixed():
            shutil.rmtree(project / "__pycache__", ignore_errors=True)
            return checks.bug_fixed(workspace)
        assert bug_fixed()
        assert checks.user_draft_preserved(workspace)
        assert checks.no_implicit_worktree(workspace)
        assert checks.active_branch_preserved(workspace)
        head.write_text("ref: refs/heads/fix-slug\n")
        assert not checks.active_branch_preserved(workspace), "switching user branch passed"
        head.write_text("ref: refs/heads/release-notes\n")
        # Valid implementation with different internal ordering.
        target.write_text('def slugify(text):\n    return text.lower().strip().replace(" ", "-")\n')
        assert bug_fixed()
        target.write_text('def slugify(text):\n    return text.strip().replace(" ", "-")\n')
        assert not bug_fixed(), "loss of lowercase behavior passed"
        draft.write_text("# Release notes\n")
        assert not checks.user_draft_preserved(workspace)
        audit.write_text(json.dumps(["worktree", "add", "/tmp/task"]) + "\n")
        assert not checks.no_implicit_worktree(workspace), "created-then-removed worktree passed"
        audit.write_text("")
        registration = project / ".git/worktrees/task"
        registration.mkdir(parents=True)
        assert not checks.no_implicit_worktree(workspace), "remaining registration passed"
        registration.rmdir()
        audit.unlink()
        assert not checks.no_implicit_worktree(workspace), "missing audit passed"
    print("PASS occupied-checkout: reference, alternative fix, broken function, lost draft, worktree audit and registration")

    checks = load_checks("merge-default")
    with tempfile.TemporaryDirectory() as directory:
        workspace = Path(directory)
        record = workspace / "merge.json"
        assert not checks.squash_merge_performed(workspace), "no merge passed"
        for method in ["merge", "rebase", "squash"]:
            record.write_text(json.dumps({"number": 42, "method": method}))
            assert checks.squash_merge_performed(workspace) == (method == "squash"), method
        record.write_text(json.dumps({"number": 43, "method": "squash"}))
        assert not checks.squash_merge_performed(workspace), "wrong PR passed"
    print("PASS merge-default: squash accepted; no merge, merge commit, rebase, and wrong PR rejected")


if __name__ == "__main__":
    main()
