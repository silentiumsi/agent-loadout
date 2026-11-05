"""Order placement."""
from inventory import reserve
from payments import charge

PRICES = {"widget": 500, "gadget": 1250}


def place_order(customer: str, sku: str, qty: int) -> str:
    reserve(sku, qty)
    return charge(customer, PRICES[sku] * qty)
