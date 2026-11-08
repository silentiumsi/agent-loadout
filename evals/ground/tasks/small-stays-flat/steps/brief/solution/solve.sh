#!/bin/bash
set -euo pipefail
mkdir -p /app/ground
mkdir -p /app/ground/$(dirname design.md)
cat > /app/ground/design.md <<'REF0'
# Design

(proposed) A single pass reads the header, skips the alignment row, then splits each row on unescaped pipes.
REF0
mkdir -p /app/ground/$(dirname product.md)
cat > /app/ground/product.md <<'REF1'
# tabcsv

tabcsv turns one Markdown table, read from standard input, into CSV on standard output. It handles alignment rows and escaped pipes, takes no config file, and accepts no flag except --delimiter.

## Acceptance checks
- A table with an alignment row produces CSV without that row.
- An escaped pipe appears as a pipe inside its cell.
- --delimiter changes the separator, and no other flag is accepted.
REF1
