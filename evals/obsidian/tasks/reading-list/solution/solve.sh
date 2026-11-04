#!/bin/bash
set -euo pipefail

note="/root/Documents/Notes/Lists/Weekend Reading.md"

cat > "$note" <<EOF
---
tags: [list, books]
created: $(date +%F)
---
# Weekend Reading

- A Wizard of Earthsea by Ursula K. Le Guin
- Kindred by Octavia E. Butler
- The Hobbit by J. R. R. Tolkien
EOF
