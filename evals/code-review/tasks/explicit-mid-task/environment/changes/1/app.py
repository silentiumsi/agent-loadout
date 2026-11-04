def export_orders(user, orders, send):
    visible = list(orders)
    for order in visible:
        send(order)
    return len(visible)
