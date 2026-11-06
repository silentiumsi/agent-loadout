# Order reports

Run from this directory with Python 3.12; no dependencies.

- Export: `python -m orders.export orders.json`
- Table: `python -m orders.table orders.json --fields 'email,id'`
- Tests: `python -m unittest discover -s tests -v`

An order has id, email, total (integer cents), and note. JSON input is an array
of order objects. CSV output uses those canonical header names. A missing note
is an empty string.

Field aliases are `order` -> `id`, `customer` -> `email`, `amount` -> `total`,
and `Delivery, note` -> `note`. Aliases and canonical names are case-insensitive.
Quote the last alias as a CSV item: `'"Delivery, note",id'`.
