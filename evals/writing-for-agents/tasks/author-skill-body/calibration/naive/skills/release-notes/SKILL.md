---
name: release-notes
description: Helps write release notes. Use this skill whenever a release happens, a tag is created, or someone mentions releases or changelogs.
version: 1.0
---

# Release Notes

Release notes tell customers what changed in a release. Follow a Keep a Changelog style.
Be accurate and concise, double-check your work, use a professional tone, and write clearly.

Run `python tools/notes.py draft --since PREVIOUS_TAG` to get the entries. Group them by impact
and put the notes in `releases/`. Avoid internal ticket IDs like ENG-1234.
