from datetime import timedelta

REFUND_WINDOW = timedelta(days=14)


class RefundError(Exception):
    pass


def refund(order, amount, now):
    if now - order["captured_at"] > REFUND_WINDOW:
        raise RefundError("outside refund window")
    remaining = order["captured"] - order["refunded"]
    if amount > remaining:
        raise RefundError("exceeds remaining")
    order["refunded"] += amount
    return order["refunded"]
