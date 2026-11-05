Triage the open issues in $ARGUMENTS and output one line per issue that needs attention.

Each line is a bare JSON object with exactly these keys:

- `id`: the issue number, as an integer
- `severity`: `p0` (blocks customers or loses data), `p1` (degrades a main flow), or `p2` (minor)
- `summary`: what is wrong, at most 80 characters

Example output, two lines:

{"id": 412, "severity": "p0", "summary": "Checkout returns 500 for carts over 50 items"}
{"id": 421, "severity": "p1", "summary": "Export takes about 40 seconds on large accounts"}

Output only those lines. Do not add prose, headings, a table, or a code fence: another tool reads
every line and rejects anything that is not one of these objects. If there are no issues to report,
output nothing.
