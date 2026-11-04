# Skill evaluations

Compare Codex and Claude Code with and without local Loadout skills to see
whether the skills improve their results. Each evaluation runs tasks in
containers and scores the results using automated checks.

Each skill directory's `CASES.md` lists its cases, why they exist, and what the
checks can establish.

## Setup

You need Docker running and Harbor installed. These configs were validated
with Harbor `0.24.1.dev202610240342`.

Authenticate both agents using your subscriptions:

- Run `codex login`.
- Run `claude setup-token` and export the returned token as
  `CLAUDE_CODE_OAUTH_TOKEN` in the terminal where you run Harbor.

## Run

Choose a skill directory under `evals/`. From the repository root, replace
`<skill>` with that directory’s name:

```sh
# With the local skill
harbor run --config evals/<skill>/with-skill.yaml

# Baseline: the same tasks and models without the skill
harbor run --config evals/<skill>/baseline.yaml
```

### Defaults

Each job runs one attempt per task and agent, one trial at a time.

### Optional overrides

For three attempts per task and agent, with two trials running at a time:

```sh
harbor run --config evals/<skill>/with-skill.yaml --n-attempts 3 --n-concurrent 2
```

Use the same overrides for the baseline. Add `--print-config` to either command
to inspect its settings without running trials.

## Read the results

Open `jobs/<job>/result.json` for the job summary. Each trial includes agent
logs, scores in `verifier/reward.json`, and individual check results in
`verifier/reward-details.json`. Higher scores are better; 1 means all automated
checks passed. Compare each task and agent across the skill and baseline jobs.

Scores reflect only the automated checks. Review the agent logs alongside
them to assess behavior the checks may not cover.

For multi-step tasks, each turn's logs, artifacts, and verifier results are
under `steps/<step>/` within the trial directory. Check those scores to see
where the conversation went wrong; the trial score averages the steps.
