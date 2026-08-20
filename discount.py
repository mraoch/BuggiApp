"""buggy-app: a tiny discount-calculator service used as the demo codebase."""

from decimal import Decimal, InvalidOperation


def apply_discount(price, percent):
    """Return price after applying a percentage discount.

    Args:
        price (str | number): the original price.
        percent (number): discount percentage (0-100).
    """
    try:
        price = Decimal(str(price))
    except InvalidOperation as exc:
        raise ValueError(f"invalid price: {price!r}") from exc

    if price < 0:
        raise ValueError("price cannot be negative")

    if percent < 0 or percent > 100:
        raise ValueError("discount percent must be between 0 and 100")

    multiplier = 1 - Decimal(percent) / 100
    return (price * multiplier).quantize(Decimal("0.01"))
