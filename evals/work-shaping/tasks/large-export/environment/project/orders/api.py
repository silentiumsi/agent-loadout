from orders.csv_export import render_csv

def list_orders(request, store):
    return store.orders(tenant_id=request.tenant_id, since=request.query.get("since"), limit=5000)

def support_export(request, store):
    return render_csv(list_orders(request, store))
