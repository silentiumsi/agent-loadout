def import_rows(tenant_id, rows, store):
    for row in rows:
        store.upsert(tenant_id, row["id"], row)
