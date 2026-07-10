from decimal import Decimal, ROUND_HALF_UP


def round_to_tick(price: float, tick_size: float = 0.05) -> float:
    """
    Round a price to the nearest valid tick.

    Examples:
        round_to_tick(242.300003, 0.01) -> 242.30
        round_to_tick(242.33, 0.05)     -> 242.35
        round_to_tick(242.32, 0.05)     -> 242.30
    """
    price = Decimal(str(price))
    tick = Decimal(str(tick_size))

    rounded = (price / tick).quantize(
        Decimal("1"),
        rounding=ROUND_HALF_UP
    ) * tick

    return float(rounded)


def floor_to_tick(price: float, tick_size: float = 0.05) -> float:
    """
    Round down to the nearest valid tick.

    Useful for BUY LIMIT orders if you never want to pay above LTP.
    """
    price = Decimal(str(price))
    tick = Decimal(str(tick_size))

    rounded = (price // tick) * tick
    return float(rounded)


def ceil_to_tick(price: float, tick_size: float = 0.05) -> float:
    """
    Round up to the nearest valid tick.

    Useful for SELL LIMIT orders.
    """
    price = Decimal(str(price))
    tick = Decimal(str(tick_size))

    rounded = ((price + tick - Decimal("0.000000001")) // tick) * tick
    return float(rounded)


def is_valid_tick(price: float, tick_size: float = 0.05) -> bool:
    """
    Check whether a price is already a valid multiple of the tick size.
    """
    price = Decimal(str(price))
    tick = Decimal(str(tick_size))

    return (price % tick) == Decimal("0")


def format_price(price: float, tick_size: float = 0.05) -> float:
    """
    Convert any floating-point value into a valid exchange price.

    This should be called before every order placement.
    """
    return round_to_tick(price, tick_size)
