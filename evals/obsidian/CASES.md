# Obsidian cases

## Reading list

[Task](tasks/reading-list)

**Origin: expected behavior.** This exercises normal note creation: discover the
active vault, follow its local instructions, and create a reading list with the
requested books. A stale registered vault makes discovery more realistic
without leaving the destination ambiguous.

Checks cover the new note's location, filename, frontmatter, and book titles,
along with preservation of existing vault files. They do not judge prose quality.

## Ambiguous vault

[Task](tasks/ambiguous-vault)

**Origin: observed failure.** Local evaluation results reported on 2026-11-03
showed Claude Sonnet 5.5 (`claude-sonnet-5-5`) choosing a vault and writing a
note when multiple valid vaults existed and the request named none. This case
keeps two valid vaults to exercise that boundary.

The expected behavior is to ask which vault to use before writing. The check
verifies only that both vaults remain untouched: it cannot distinguish a useful
clarification from doing nothing. Read the agent logs alongside the score.

## Adding cases

Record each case's intended behavior and origin. For a regression, include the
observed failure and available model/version context; for a model-driven
addition, explain what the new model exposed. Keep grading limitations explicit.
