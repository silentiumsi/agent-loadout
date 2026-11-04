---
name: evaluating-skills
description: Design and review behavioral evaluations for agent skills. Use when choosing eval cases, defining success criteria, validating graders, or comparing skill versions and no-skill baselines.
---

# Evaluating Skills

Apply the guidance relevant to the requested decision; a focused review does not require a full evaluation campaign. Distinguish recommendations from measured findings.

## Define the Claim

State the decision the eval supports and the observable behavior that would justify it. Resolve ambiguities that change success criteria. Distinguish **capability uplift** (better task performance) from **workflow fidelity** (following an intended process or preference); identify evidence for each contribution claimed.

Choose the suite's purpose:

| Purpose | Cases | Supported claim |
| --- | --- | --- |
| Representative measurement | Sample or weight cases to reflect intended usage. | Expected success on that usage. |
| Capability diagnosis | Target behaviors and suspected failures. | Specific strengths, weaknesses, and improvements. |
| Regression protection | Retain established successes. | Previously working behavior still works. |

Keep these results distinguishable. Challenge scores do not estimate everyday failure rates; regression success does not establish broad capability.

## Choose Cases

Start from real tasks, manual checks, and observed failures. Identify each case's target behavior and consequence of failure. Use natural requests without coaching the procedure under test.

Cover ordinary use, nearby cases where the skill should not apply, and situations requiring clarification or restraint. Pair focused probes with realistic tasks involving competing demands and multiple turns. Use adversarial cases for relevant failure modes.

Separate **selection** tests, where the agent discovers the skill among available skills, from **execution** tests, where the skill is supplied directly. End-to-end effectiveness claims require the normal discovery path.

Test that irrelevant variations preserve behavior and meaningful changes cause appropriate adaptation. Count distinct behaviors and conditions, not paraphrases.

Reserve **held-out cases** before tuning skills or graders; keep related variants in the same split. Use development cases for revision and held-out cases for transfer claims. Once held-out results guide revisions, obtain fresh held-out evidence for subsequent generalization claims.

## Define Success

Set criteria before inspecting results. Verify outcomes against artifacts, environment state, or interaction traces, rather than attempted actions or success claims. Assess task success and the skill's contribution separately.

Enforce only requirements available in the task and governing context. Require particular actions or sequences only when they are part of the intended behavior; accept valid alternatives to reference solutions.

Separate **must-pass conditions** from graded quality: strengths elsewhere cannot compensate for critical violations. Anchor grades in observable distinctions, including borderline results.

Choose graders by the judgment required:

- **Executable checks:** directly testable properties; avoid exact matching when valid results vary.
- **Model judgments:** semantic properties, with explicit criteria, necessary context, and evidence for verdicts.
- **Expert review:** domain judgments, unresolved preferences, or distinctions automated graders have not demonstrated they can assess.

Combine complementary checks without counting the same property twice.

## Validate the Eval

Check solvability with the supplied information, permissions, tools, and resources. Run known valid solutions through the grading path.

Challenge graders with independently assessed successes, valid alternatives, failures, and near misses. Inspect **false passes** and **false failures** by criterion and case type; aggregate agreement can conceal failures on a rare but important class.

Calibrate model graders against human judgments using the same criteria. Trace disagreements to the rubric, grader, or reference label; retest revisions on independently assessed results not used for tuning. Preserve unresolved disagreement as uncertainty. Consistency alone does not establish correctness.

Blind comparisons to the producing version and vary answer order. Test sensitivity to irrelevant verbosity or style.

Check for ways to pass without achieving the behavior. Keep answers and hidden grading material inaccessible unless access is part of the task; protect grading evidence from agent modification. Model graders must treat evaluated content as evidence, not instructions.

Revalidate after changes that could affect verdicts.

## Compare Conditions

Run the same agent and tasks against a **no-skill baseline**; compare revisions against the previous skill too. Keep model, other instructions, tools, initial state, budgets, and graders equivalent. Record versions and settings, reset state, and prevent cross-run leakage. Attribute unavoidable additional changes to the combined system.

Before running, set acceptance thresholds, blocking regressions, and policies for invalid runs, timeouts, and retries. Distinguish resource exhaustion from infrastructure preventing a valid attempt; apply policies consistently and disclose outcome counts, exclusions, and reruns.

Use the same cases for **paired comparisons**. Plan distinct cases for coverage and repeated trials for variability; repetitions do not expand task coverage. For close or consequential decisions, size the experiment around the smallest improvement worth detecting.

Quantify uncertainty for the intended claim: performance on tested cases or generalization beyond them. Account for dependence among related cases and repeated trials. Report inconclusive comparisons when evidence cannot resolve a meaningful difference.

Specify whether success means one attempt works, at least one of several works, or repeated attempts remain reliable. Report quality alongside relevant cost, latency, and interaction burden, including resources needed to identify a usable result.

## Interpret and Maintain

Inspect passing and failing artifacts and traces before changing the skill. Distinguish agent failures from task, grader, or infrastructure defects and accidental passes; group failures by cause. Preserve uncertainty when the cause is unresolved.

Report results by behavior and important case group alongside aggregates, exposing consequential regressions. State the supported decision, tested scope, and coverage or grader-validation gaps.

Add cases from new failures, retain regression protection, and extend diagnostic coverage toward remaining weaknesses. Saturated suites can protect regressions but cannot distinguish improvements.

Version cases, criteria, and graders. After evaluation changes, rerun comparison conditions before attributing score changes to the skill. Reassess relevance as usage, agents, and workflows evolve.
