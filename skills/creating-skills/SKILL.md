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

## Writing the Body

Write the instructions with `writing-for-agents`: what to keep, how to state authority and completion, and how to lead with what the agent needs. Load it before drafting the body.

Put branch-specific detail in `references/` and link it from the body with the condition for reading it. Keep skills durable: ground them in task constraints and required capabilities, not model-specific workarounds or private tool names.

## Final Cut Pass

Run a **blind review** with a fresh-context subagent. Give it only the skill and its supporting files, withholding the drafting conversation and rationale. Ask it to assess what the skill communicates on its own: unnecessary structure, unclear instructions, repetition, gaps, and whether leading words carry the intended behavior and replace repeated explanations. Require located findings and targeted suggestions, without direct edits. Use the findings to revise the skill, preserving required behavior and keeping text only when its omission would cause a distinct, plausible failure. If fresh-context review is unavailable, report that it could not run.

Where practical, try the skill against an available example identified before drafting. Give the agent the skill and the example task without coaching it toward the expected behavior, then compare its actions with the intended behavior change. Use any mismatch to guide revision; report when this check could not run.
