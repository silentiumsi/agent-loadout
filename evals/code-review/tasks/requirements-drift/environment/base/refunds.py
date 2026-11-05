class RefundError(Exception):
    pass


def refund(order, amount, now):
    remaining = order["captured"] - order["refunded"]
    if amount > remaining:
        raise RefundError("exceeds remaining")
    order["refunded"] += amount
    return order["refunded"]
