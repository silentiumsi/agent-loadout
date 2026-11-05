"""Card payments."""

DECLINED = {"cus_declined"}


class PaymentError(Exception):
    pass


def charge(customer: str, cents: int) -> str:
    if cents <= 0 or customer in DECLINED:
        raise PaymentError(f"charge failed for {customer}")
    return f"ch_{customer}_{cents}"
