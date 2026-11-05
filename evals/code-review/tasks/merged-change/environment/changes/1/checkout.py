def total(prices_cents):
    return sum(prices_cents)


def apply_discount(price_cents, percent):
    return price_cents - price_cents * percent // 100


def price_with_coupon(price_cents, coupon):
    """Coupons look like SAVE15 and are typed into the checkout form."""
    return apply_discount(price_cents, int(coupon.removeprefix("SAVE")))
