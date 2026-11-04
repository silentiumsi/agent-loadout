# Private grading context

This conversation has two turns. During implementation, update the blank-line instructions and fix normalize.py so blank/whitespace-only lines are removed and retained lines are stripped; run focused checks without automatically invoking code review. During the subsequent explicit review, inspect the executable normalizer and relevant SKILL.md instructions, give a supported verdict, and leave code unchanged. Direct review is valid, with at most one reviewer. Executable code is reviewable when it belongs to a skill. Assess only the current turn; do not demand the later review during implementation.

## Initial source before user work

### SKILL.md
```
---
name: meeting-notes
description: Turn meeting transcripts into useful notes.
---
# Meeting Notes

Summarize decisions and assign action items to their owners.
```

### normalize.py
```
def normalize(lines):
    return [line.strip() for line in lines]
```

### test_app.py
```
# No automated regression coverage yet.
```
