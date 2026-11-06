"""Print selected order fields as JSON arrays."""

import argparse
import json
from pathlib import Path

from orders.fields import resolve_fields


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--fields")
    args = parser.parse_args()
    try:
        fields = resolve_fields(args.fields)
    except ValueError as exc:
        parser.error(str(exc))

    rows = json.loads(args.input.read_text())
    print(json.dumps([[row.get(field, "") for field in fields] for row in rows]))


if __name__ == "__main__":
    main()
