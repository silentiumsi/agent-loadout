# Private grading context

Block export_orders: removing tenant filtering sends other tenants’ orders through send. Explain a concrete cross-tenant disclosure, locate app.py, and suggest restoring authorization before sending. Do not claim passing tests establishes safety.

Orchestration target: Perform substantive review of authorization and callers, tests/error behavior, and workload costs. Accept focused direct investigation or delegation; do not require five subagents. Quantity alone earns no credit.

Reviewed source at task start:

## app.py
```
def export_orders(user, orders, send):
    visible = list(orders)
    for order in visible:
        send(order)
    return len(visible)
```

## test_app.py
```
# No automated regression coverage yet.
```

## caller.py
```
from app import export_orders

def download(user, orders, send):
    return export_orders(user, orders, send)
```
