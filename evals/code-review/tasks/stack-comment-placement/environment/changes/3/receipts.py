"""Receipt formatting."""


def format_receipt(charge_id: str, cents: int) -> str:
    return f"Receipt {charge_id}: ${cents // 100}.{cents % 100:02d}"
