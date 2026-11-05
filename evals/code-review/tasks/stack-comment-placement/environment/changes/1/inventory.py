"""Stock levels per SKU."""

STOCK: dict[str, int] = {}


def add_stock(sku: str, qty: int) -> None:
    STOCK[sku] = STOCK.get(sku, 0) + qty


def available(sku: str) -> int:
    return STOCK.get(sku, 0)


def reserve(sku: str, qty: int) -> None:
    STOCK[sku] = STOCK.get(sku, 0) - qty


def release(sku: str, qty: int) -> None:
    STOCK[sku] = STOCK.get(sku, 0) + qty
