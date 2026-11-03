# Loadout

Reusable skills for Claude Code and Codex, distributed as the `loadout` plugin.

This repository is private while third-party attribution is completed. Keep it
private until the README attribution has been reviewed and publication explicitly
authorized. Original work is licensed under [MIT](LICENSE); third-party work
retains its applicable license and attribution requirements.

## Skills

All skills and supporting files live in `skills/`.

| Skill | Purpose |
| --- | --- |
| `code-review` | Review changes with independent reviewers across five dimensions. |
| `creating-skills` | Write and maintain agent skills. |
| `debugging-and-error-recovery` | Trace failures to their cause and verify the repair. |
| `git-workflow` | Organize branches, save points, and review requests. |
| `grilling` | Settle decisions through rounds of concrete questions. |
| `interactive-writing` | Write artifacts in agreed increments with an editor. |
| `obsidian` | Find and maintain notes in locally configured Obsidian vaults. |
| `scratch` | Place disposable files in a locally ignored `.scratch/` directory. |

These skills carry opinionated workflows. Obsidian operations require Obsidian
and `jq` on Linux or macOS. Skills that delegate work require an agent host with
subagent support. No MCP servers or API keys are required to install Loadout.

## Install

While this repository is private, Git access to `silentiumsi/agent-loadout` is
required.

Claude Code:

```sh
claude plugin marketplace add silentiumsi/agent-loadout
claude plugin install loadout@loadout
```

Codex:

```sh
codex plugin marketplace add silentiumsi/agent-loadout
codex plugin add loadout@loadout
```

Restart the client and begin a new session after installation.

## Update

Claude Code:

```sh
claude plugin marketplace update loadout
claude plugin update loadout@loadout
```

Codex:

```sh
codex plugin marketplace upgrade loadout
codex plugin add loadout@loadout
```

Restart the client after updating. If an old cached copy persists, remove and
reinstall `loadout@loadout` using the same installation scope.

## Maintain

Edit skills here; this repository is their authoritative source. Keep `version`
in `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` in sync, increment
both when releasing a change, and commit and push the manifests with the skills.
Tag releases as `v<version>` so consumer catalogs can pin a release.

Validate the Claude Code package and marketplace before releasing:

```sh
claude plugin validate .claude-plugin/plugin.json --strict
claude plugin validate .claude-plugin/marketplace.json --strict
```

See the [Claude Code marketplace reference](https://code.claude.com/docs/en/plugin-marketplaces)
and [OpenAI plugin packaging documentation](https://developers.openai.com/plugins/build/plugins)
for the two package formats.

## Attribution

Third-party attribution is pending a separate README review. This extraction
preserves the existing skills and supporting files. Complete the source and
license acknowledgments before making this repository public.
