from receipts import format_receipt


def test_format_receipt():
    assert format_receipt("ch_1", 1250) == "Receipt ch_1: $12.50"
