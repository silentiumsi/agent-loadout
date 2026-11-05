import inventory
from orders import place_order


def setup_function():
    inventory.STOCK.clear()


def test_place_order_charges_total_and_reserves_stock():
    inventory.add_stock("widget", 5)
    assert place_order("cus_1", "widget", 2) == "ch_cus_1_1000"
    assert inventory.available("widget") == 3
