# Notes for the agent guidance (from Dana, platform lead)

Dumping what agents keep getting wrong. Turn it into guidance in AGENTS.md.

- `kc deploy` rejects service names over 32 characters, so keep names short.
- Only deploy Tuesday to Thursday. That's our rule since the December outage
  (ADR-12), not something the tool enforces.
- CI blocks merges without tests, so don't bother pushing untested work.
- We write new code for Python 3.12. Use 3.12 features if they help.
- Regions: `kc` requires `--region`, either `eu-west` or `us-east`.
- I like conventional commits (`feat:`, `fix:`) but if the PR already uses
  another style, match that instead.
