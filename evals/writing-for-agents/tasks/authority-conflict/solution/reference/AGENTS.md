# Kestrel agent notes

## Deploying

- Deploy with `python tools/kc.py deploy NAME --region REGION`. `--region` is required and must be `eu-west` or `us-east`. Service names over 40 characters are rejected (`tools/kc.py`).
- Deploy only Tuesday to Thursday. This is the team's rule since the December outage ([ADR-12]); the tool does not enforce it, so the check is yours.

## Merging

- Tests must pass before you ask for review. This is a team convention in `CONTRIBUTING.md`; CI only runs lint (`.ci/pipeline.yml`), so nothing will stop untested work. Run the tests yourself.

## Defaults you may adapt

- New code targets Python 3.12 by team preference; the project itself supports 3.11 and later (`pyproject.toml`). Use 3.12 features only when they help.
- Prefer conventional commits (`feat:`, `fix:`). If the PR already uses another style, match that instead.
