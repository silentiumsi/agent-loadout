#!/bin/sh
set -eu
cd /app/project
python - <<'FIX'
from pathlib import Path
path = Path("slug.py")
path.write_text(path.read_text().replace("text.lower()", "text.strip().lower()"))
FIX
python -m unittest
