"""Export order objects as CSV."""

import argparse
import csv
import io
import json
from pathlib import Path

from orders.fields import DEFAULT_FIELDS


def render_csv(rows):
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(DEFAULT_FIELDS)
    writer.writerows([row.get(field, "") for field in DEFAULT_FIELDS] for row in rows)

    return output.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()

    rows = json.loads(args.input.read_text())
    print(render_csv(rows), end="")


if __name__ == "__main__":
    main()
