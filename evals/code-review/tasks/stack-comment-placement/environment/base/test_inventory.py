import inventory


def setup_function():
    inventory.STOCK.clear()


def test_add_stock():
    inventory.add_stock("widget", 3)
    assert inventory.available("widget") == 3
