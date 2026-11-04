#!/bin/bash
set -euo pipefail
python3 - <<'EDIT'
from pathlib import Path
p = Path('/app/guide.md')
s = p.read_text()
start = s.index('## Detection') + len('## Detection')
end = s.index('## Escalation', start)
s = s[:start] + '\n\nAt 09:00 UTC look at the Willow dashboard, if the outage lasts ten minutes tell duty@example.test about it. Don’t contact the vendor.\n\n' + s[end:]
p.write_text(s)
EDIT
