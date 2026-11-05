---
name: release-notes
description: Write public release notes for a tagged release. Use only when the user asks for release notes by name.
disable-model-invocation: true
---

# Release Notes

1. Draft from the previous tag: `python tools/notes.py draft --since PREVIOUS_TAG`. It prints JSON with `entries` and `warnings` and exits 0 either way. Read `warnings`: a nonempty list means the draft is incomplete (usually an untagged commit). Resolve each, or report it, before going on.
2. Give each entry an impact from `docs/impact-tags.md`. Group by impact, `breaking` first. Leave `internal` out.
3. Write the customer-facing change for each entry. Never include internal ticket IDs such as `ENG-1234`; say what changed for the customer instead.
4. Save to `releases/vX.Y.Z.md`. Never edit `CHANGELOG.md`; it is generated.

Done when the notes file exists, `warnings` is empty or reported, and no `ENG-` ID appears in it.
