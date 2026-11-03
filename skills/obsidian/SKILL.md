---
name: obsidian
description: >-
  Find, read, create or edit Obsidian notes, including daily notes and second-brain
  records. Also use to save durable output with no project home or named path.
  Not for project files or disposable output.
---
# Obsidian

## Locate

Use the named vault; otherwise run `sh scripts/get-vaults.sh` from this skill's
root. Report discovery failures; ask which vault if several exist.

Search filenames before contents, starting in the smallest likely folder.
Resolve `[[note]]` by filename across the vault; missing targets need not exist.

## Write

- Write only output already chosen to be kept. Keep scratch files outside the vault.
- Read vault instructions and follow its conventions. Ask where to file a note
  when neither the request nor a convention supplies a destination.
- Reuse a matching note unless a separate record is intended. Ask if ambiguous.
- Without a naming convention, use descriptive kebab-case; date separate records
  such as daily notes.
- Never move, rename or delete notes unless asked.
- Markdown and HTML are supported. For other output, check
  [supported formats](https://obsidian.md/help/file-formats); ask before writing
  an unsupported format.

If clarification is needed and no user can answer, report the blocker without
writing. Report write failures; never silently change destination.

Read back changes to verify them. Report the vault-relative path and any
unverified checks.
