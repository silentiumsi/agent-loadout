# Release-notes skill (from Priya)

Every release I paste the commit list into chat and say "write the notes".
Agents do okay but keep getting these wrong:

- Public notes go in `releases/vX.Y.Z.md`. Never touch `CHANGELOG.md`; it is generated.
- Never put internal ticket IDs (`ENG-1234`) in public notes. Say the customer-facing change instead.
- Start from `python tools/notes.py draft --since PREVIOUS_TAG`. It prints JSON with
  `entries` and `warnings`. It exits 0 even when `warnings` is nonempty, and a
  nonempty list means the draft is incomplete (usually an untagged commit).
- Give each entry an impact from `docs/impact-tags.md` and group by impact, breaking
  first. Leave `internal` entries out.
- Be accurate and concise, double-check your work, use a professional tone, and
  write clearly.
- Keep a Changelog style is fine for the layout.
- I only want this to run when I ask for it by name. Never start it on your own
  after a tag.
