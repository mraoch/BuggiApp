import pytest

from discount import apply_discount


def test_full_price_no_discount():
    assert apply_discount("10.00", 0) == "10.00"


def test_half_price():
    assert str(apply_discount("10.00", 50)) == "5.00"


def test_string_price():
    assert str(apply_discount("20.00", 25)) == "15.00"


def test_rounds_to_cents():
    assert str(apply_discount("9.99", 10)) == "8.99"


def test_invalid_price_raises():
    with pytest.raises(ValueError):
        apply_discount("abc", 10)


def test_negative_price_raises():
    with pytest.raises(ValueError):
        apply_discount("-1", 10)


def test_percent_out_of_range_raises():
    with pytest.raises(ValueError):
        apply_discount("10.00", 101)
