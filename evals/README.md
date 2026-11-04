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

Each job runs one attempt per task and agent, with up to 16 concurrent trials.
Keep the total across simultaneous local Docker jobs at 16 trials or fewer;
verifiers also create networks and can exhaust Docker address pools.

### Optional overrides

For three attempts per task and agent, keeping the default concurrency:

```sh
harbor run --config evals/<skill>/with-skill.yaml --n-attempts 3
```

### Choose an agent and model

Run only Codex with an OpenAI model:

```sh
harbor run --config evals/code-review/with-skill.yaml \
  --agent codex --model openai/gpt-6.1-terra \
  --agent-kwarg version=0.166.0 \
  --agent-env CODEX_FORCE_AUTH_JSON=1 \
  --resume-trajectory --skill ./skills/code-review
```

Run only Claude Code with an Anthropic model:

```sh
harbor run --config evals/code-review/with-skill.yaml \
  --agent claude-code --model anthropic/claude-sonnet-5-5 \
  --agent-kwarg version=2.1.318 \
  --agent-env CLAUDE_FORCE_OAUTH=1 \
  --resume-trajectory --skill ./skills/code-review
```

Replace the model identifier to test another model supported by that agent.
`--agent` replaces the config's agent list; these examples explicitly restore
its CLI version, subscription settings, conversation resumption, and local skill.
The task's configured verifier model stays unchanged.

### Choose one task

Run only `high-risk` from the code-review suite, keeping both configured agents:

```sh
harbor run --config evals/code-review/with-skill.yaml \
  --path evals/code-review/tasks/high-risk
```

Add the same `--path` option to either model example to select both a model and
a task. Use the task directory's path; `--task` selects a registry task instead.

For baseline comparisons, use `baseline.yaml` with the same overrides and omit
`--skill` from the model examples. Add `--print-config` to any command to inspect
its resolved tasks, models, and skill availability without running trials.

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
