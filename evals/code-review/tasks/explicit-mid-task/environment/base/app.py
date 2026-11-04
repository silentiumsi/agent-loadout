def export_orders(user, orders, send):
    visible = [o for o in orders if o["tenant"] == user["tenant"]]
    for order in visible:
        send(order)
    return len(visible)
