"""Export order objects as CSV."""

import argparse
import csv
import io
import json
from pathlib import Path

from orders.fields import DEFAULT_FIELDS, resolve_fields


def render_csv(rows, fields=DEFAULT_FIELDS):
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(fields)
    writer.writerows([row.get(field, "") for field in fields] for row in rows)

    return output.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--columns")
    args = parser.parse_args()
    try:
        fields = resolve_fields(args.columns)
    except ValueError as exc:
        parser.error(str(exc))

    rows = json.loads(args.input.read_text())
    print(render_csv(rows, fields), end="")


if __name__ == "__main__":
    main()
