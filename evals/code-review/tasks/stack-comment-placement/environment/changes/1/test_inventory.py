import inventory


def setup_function():
    inventory.STOCK.clear()


def test_add_stock():
    inventory.add_stock("widget", 3)
    assert inventory.available("widget") == 3


def test_reserve_reduces_stock():
    inventory.add_stock("widget", 5)
    inventory.reserve("widget", 2)
    assert inventory.available("widget") == 3


def test_release_restores_stock():
    inventory.add_stock("widget", 5)
    inventory.reserve("widget", 2)
    inventory.release("widget", 2)
    assert inventory.available("widget") == 5
