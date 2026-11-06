"""Shared field-selection policy for order reports."""

import csv
import io

DEFAULT_FIELDS = ("id", "email", "total", "note")
ALIASES = {name: name for name in DEFAULT_FIELDS} | {
    "order": "id", "customer": "email", "amount": "total", "delivery, note": "note",
}


def resolve_fields(raw):
    if raw is None:
        return DEFAULT_FIELDS

    try:
        records = list(csv.reader(io.StringIO(raw), strict=True, skipinitialspace=True))
    except csv.Error as exc:
        raise ValueError(f"invalid field selection: {exc}") from exc

    if len(records) != 1 or not records[0]:
        raise ValueError("select one nonempty record of fields")

    selected = []
    for field in records[0]:
        key = field.strip().casefold()
        if key not in ALIASES:
            raise ValueError(f"unknown or empty field: {field!r}")

        canonical = ALIASES[key]
        if canonical not in selected:
            selected.append(canonical)

    return tuple(selected)
