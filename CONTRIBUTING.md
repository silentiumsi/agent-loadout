# Contributing

## Maintain

Edit skills here; this repository is their authoritative source. Installations
follow `main`.

Install the secret-scanning hooks after cloning. They need
[lefthook](https://github.com/evilmartians/lefthook) and Go, which runs the
version of [Betterleaks](https://github.com/betterleaks/betterleaks) pinned in
`lefthook.yml`:

```sh
lefthook install
```

Commits are checked for staged secrets, and pushes scan the full history.

Releases are manual:

1. Update `version` in `.claude-plugin/plugin.json` and
   `.codex-plugin/plugin.json`, keeping both values in sync.
2. Validate the package and marketplace using the commands below.
3. Commit and push the manifests with the skills to `main`.
4. Optionally tag the commit as `v<version>` and push the tag to mark the release.

No CI workflow, GitHub Release, or package registry upload is required.

Validate the Claude Code package and marketplace before releasing:

```sh
claude plugin validate .claude-plugin/plugin.json --strict
claude plugin validate .claude-plugin/marketplace.json --strict
```

See the [Claude Code marketplace reference](https://code.claude.com/docs/en/plugin-marketplaces)
and [OpenAI plugin packaging documentation](https://developers.openai.com/plugins/build/plugins)
for the two package formats.
