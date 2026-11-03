---
name: creating-skills
description: Write agent skills. Use when creating a skill, revising SKILL.md instructions, or organizing supporting scripts, references, and assets.
---

# Creating Skills

## Establish the Behavior

Before drafting, identify the task the skill should handle, what the agent would plausibly get wrong without it, and what it should do instead. Ground this in the user's requirements and available examples of success or failure. When an example is available, select one for the later behavior trial. Use the resulting behavior changes to decide what guidance belongs in the skill; ask about missing requirements when they would change those decisions.

## Skill Structure

A skill is a folder containing `SKILL.md` and any supporting files it needs.

```text
skill-name/
  SKILL.md     # Required: skill instructions and frontmatter
  scripts/     # Optional: executable helpers
  references/  # Optional: documentation read as needed
  assets/      # Optional: templates and other files used in output
```

Include a script when it avoids repeatedly recreating the same code or makes a fragile operation reliable.

## SKILL.md Format

Start with YAML frontmatter, followed by Markdown instructions:

```yaml
---
name: creating-skills
description: Write agent skills. Use when creating a skill, revising SKILL.md instructions, or organizing supporting scripts, references, and assets.
---
```

- **`name`:** Match the folder name. Use lowercase letters, digits, and hyphens.
- **`description`:** State what the skill does and the distinct situations that should trigger it. Use words likely to appear in requests. Collapse synonymous triggers. Add exclusions only when they prevent likely confusion with other skills.

The name and description are available during skill selection; the body is loaded when the skill is used. Put workflow instructions in the body.

Add other frontmatter fields only when the target environment supports them and the skill needs them.

Choose headings that fit the skill’s task. Use numbered steps when order matters; otherwise organize by decisions, topics, or operating modes.

## Writing Principles

1. **Keep only behavior-changing guidance.** For each instruction, ask what the agent would plausibly do wrong without it. Delete it if there is no concrete answer. Remove generic contracts, obvious mechanics, and explanatory restatements. Replace duplicated detail from scripts or authoritative references with a link and a clear condition for consulting the source when the agent still needs that information. Cut sections before shortening sentences.

2. **Use leading words.** A leading word is a compact, familiar concept that steers how the agent thinks and acts. During drafting, actively look for repeated explanations or clusters of instructions that a leading word could carry. Consider familiar concepts whose existing associations evoke the intended behavior, such as “tracer bullet” for a small implementation that proves a path through the system. Choose terms that carry that behavior more effectively than the descriptions they replace. Define any skill-specific meaning at first use, then repeat the term consistently. Use the same vocabulary in the skill's description and related guidance where it helps the agent recognize when to use them.

3. **A picture is worth a thousand words.** Use an example or small diagram when it conveys the intended behavior more effectively than prose. Let it replace the explanation; retain prose only for constraints it cannot carry.

4. **Make the desired behavior clear.** Use direct verbs. When describing a mistake or setting a boundary, explain what to do instead.

5. **Be specific where it matters.** Preserve constraints that affect correctness; leave routine execution to the agent. Prescribe exact mechanics only when correctness depends on them. A possible edge case alone does not justify another rule.

6. **Make completion checkable.** State only task-specific completion evidence. Do not add an Input/Output/Stop section or generic verification ceremony unless it resolves real ambiguity. Report checks that could not run as unverified.

7. **Put information where it is needed.** Keep essential guidance inline and branch-specific detail behind references with clear reading conditions. Group related rules and caveats; keep each instruction in one authoritative place.

8. **Use failure tables selectively.** For recurring or demonstrated mistakes, show the temptation, why it fails, and what to do instead. Place the table beside the relevant guidance. Prefer structural enforcement when it can prevent the mistake reliably.

9. **Write durable procedures.** Ground instructions in task constraints and required capabilities. Avoid model-specific workarounds and private tool names.

## Final Cut Pass

Run a **blind review** with a fresh-context subagent. Give it only the skill and its supporting files, withholding the drafting conversation and rationale. Ask it to assess what the skill communicates on its own: unnecessary structure, unclear instructions, repetition, gaps, and whether leading words carry the intended behavior and replace repeated explanations. Require located findings and targeted suggestions, without direct edits. Use the findings to revise the skill, preserving required behavior and keeping text only when its omission would cause a distinct, plausible failure. If fresh-context review is unavailable, report that it could not run.

Where practical, try the skill against an available example identified before drafting. Give the agent the skill and the example task without coaching it toward the expected behavior, then compare its actions with the intended behavior change. Use any mismatch to guide revision; report when this check could not run.
