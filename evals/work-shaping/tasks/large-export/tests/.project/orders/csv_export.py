import csv
import io

def render_csv(rows):
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=["id", "created_at", "total"])
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue()
