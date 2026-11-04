# Obsidian cases

## Ambiguous vault

[Task](tasks/ambiguous-vault)

**Origin: observed failure.** Local evaluation results reported on 2026-11-03
showed Claude Sonnet 5.5 (`claude-sonnet-5-5`) choosing a vault and writing a
note when multiple valid vaults existed and the request named none. This case
keeps two valid vaults to exercise that boundary.

The expected behavior is to ask which vault to use before writing. The check
verifies only that both vaults remain untouched: it cannot distinguish a useful
clarification from doing nothing. Read the agent logs alongside the score.
