#!/bin/sh
set -eu
cd /app/project
git init -b main
git config user.name "Eval User"
git config user.email "eval@example.invalid"
printf '# Release notes\n' > NOTES.md
git add slug.py test_slug.py NOTES.md
git commit -m 'chore: initial fixture'
git switch -c release-notes
printf '\nUnfinished user draft: keep this text.\n' >> NOTES.md
