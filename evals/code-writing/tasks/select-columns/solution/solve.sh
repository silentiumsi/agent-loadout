#!/bin/bash
set -eu
cp /solution/export.py /app/project/orders/export.py
cp /solution/test_columns.py /app/project/tests/test_columns.py
cd /app/project
python -m unittest discover -s tests -v
