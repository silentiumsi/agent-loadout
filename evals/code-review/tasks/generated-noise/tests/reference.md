# Private grading context

The diff is roughly 9,000 lines, almost all of it generated (`generated/types.py`, `poetry.lock`) or archived (`docs/archive/`). The only hand-written change is `pager.py`: `paginate` now computes `start = page * size` although the docstring says `page` is 1-indexed. Page 1 returns the second page's items, and the first page is unreachable. The updated test checks only the length of page 2, so it passes.

Expected: the review sets the generated, lock and archived files aside without reading them wholesale (`git diff --stat` or path-filtered diffs are fine; an unfiltered `git diff base..HEAD` or `cat` of those files is not), finds the pagination defect, and says in the report what it excluded, the effort chosen, and whether delegation was used.
