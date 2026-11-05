from .tax import add_tax


def prorate(amount_cents: int, days_used: int, days_in_period: int) -> int:
    # Proration for mid-period plan changes.
    return int(amount_cents * days_used / days_in_period)


def invoice_total(amount_cents: int, days_used: int, days_in_period: int, rate: float) -> int:
    return add_tax(prorate(amount_cents, days_used, days_in_period), rate)
