def add_tax(cents: int, rate: float) -> int:
    return round(cents * (1 + rate))
