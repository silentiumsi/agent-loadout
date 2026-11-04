![Loadout — white L monogram with a peach square and white wordmark on a dark background](assets/loadout-header.png)

[![Version](https://img.shields.io/github/v/tag/silentiumsi/agent-loadout?style=flat-square&label=version)](https://github.com/silentiumsi/agent-loadout/tags)
[![Claude Code](https://img.shields.io/badge/Claude_Code-compatible-D97757?style=flat-square)](#install-and-update)
[![Codex](https://img.shields.io/badge/Codex-compatible-412991?style=flat-square)](#install-and-update)

Loadout is a collection of opinionated skills for Claude Code and Codex. Install
the `loadout` plugin to give your agent repeatable workflows for everyday work.

## Install and update

Run these commands in your terminal for the client you use.

### Claude Code

Install:

```sh
claude plugin marketplace add silentiumsi/agent-loadout
claude plugin install loadout@loadout
```

Update:

```sh
claude plugin marketplace update loadout
claude plugin update loadout@loadout
```

### Codex

Install:

```sh
codex plugin marketplace add silentiumsi/agent-loadout
codex plugin add loadout@loadout
```

Update:

```sh
codex plugin marketplace upgrade loadout
codex plugin add loadout@loadout
```

Restart your client and begin a new session after installing or updating.

## Skills

| Skill | What it does |
| --- | --- |
| [code-review](skills/code-review/SKILL.md) | Reviews changes on request, scaling effort to risk, across correctness, readability, architecture, security, and performance. |
| [code-simplification](skills/code-simplification/SKILL.md) | Simplifies working code for clarity while preserving behavior. |
| [creating-skills](skills/creating-skills/SKILL.md) | Turns repeatable procedures into focused agent skills. |
| [debugging-and-error-recovery](skills/debugging-and-error-recovery/SKILL.md) | Traces failures to their root cause, repairs them, and verifies the result. |
| [documentation](skills/documentation/SKILL.md) | Writes and maintains technical documentation, cutting clutter while preserving facts and decision rationale. |
| [evaluating-skills](skills/evaluating-skills/SKILL.md) | Designs and reviews behavioral evaluations for agent skills. |
| [git-workflow](skills/git-workflow/SKILL.md) | Guides branches, commits, worktrees, and review requests. |
| [grilling](skills/grilling/SKILL.md) | Tests ideas and decisions through rounds of concrete questions. |
| [interactive-writing](skills/interactive-writing/SKILL.md) | Writes with you as editor, in agreed increments with feedback between each. |
| [obsidian](skills/obsidian/SKILL.md) | Finds, reads, and maintains notes in your local Obsidian vaults. |
| [scratch](skills/scratch/SKILL.md) | Keeps disposable task files in a locally ignored `.scratch/` directory. |
| [writing-specs](skills/writing-specs/SKILL.md) | Writes specifications that humans and agents can understand, implement, and verify. |

For maintenance and release instructions, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Evaluate skills

[Harbor evaluations](evals/README.md) test the local skills in this checkout
and compare them with runs without the skill. Start with the Obsidian eval:

```sh
harbor run --config evals/obsidian/with-skill.yaml
```

## Attribution

Loadout is inspired by:

- [Matt Pocock’s skills](https://github.com/mattpocock/skills).
- [Addy Osmani’s agent-skills](https://github.com/addyosmani/agent-skills).
- [Poteto’s pstack](https://github.com/cursor/plugins/tree/main/pstack).

All three projects are MIT-licensed. Their copyright and license notices are
preserved in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

The header and icon use a color palette inspired by
[Vesper](https://github.com/raunofreiberg/vesper).
