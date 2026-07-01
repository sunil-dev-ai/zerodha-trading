# core/instrument_helper.py

from datetime import datetime
from core.kite_client import kite


def get_option_symbol(underlying: str, strike: int, opt_type: str, expiry: str):
    """
    Fetch the exact tradingsymbol for an option contract.
    expiry can be 'current week', 'monthly', or a date (YYYY-MM-DD).
    """
    instruments = kite.instruments("NFO")

    # Resolve expiry
    expiry_dates = sorted(
        {inst["expiry"] for inst in instruments if inst["name"] == underlying})
    resolved_expiry = None

    if expiry.lower() == "current week":
        # Pick the nearest weekly expiry (usually Thursday)
        resolved_expiry = min(expiry_dates)
    elif expiry.lower() == "monthly":
        # Pick the farthest expiry in the current month
        today = datetime.today()
        monthly_expiries = [
            d for d in expiry_dates if d.month == today.month and d.year == today.year]
        if monthly_expiries:
            resolved_expiry = max(monthly_expiries)
    else:
        # Assume user gave YYYY-MM-DD
        resolved_expiry = datetime.strptime(expiry, "%Y-%m-%d").date()

    # Find matching contract
    for inst in instruments:
        if (inst["name"] == underlying and
            inst["strike"] == strike and
            inst["expiry"] == resolved_expiry and
            inst["instrument_type"] == "OPT" and
            inst["segment"] == "NFO-OPT" and
                inst["tradingsymbol"].endswith(opt_type)):
            return inst
    return None


def validate_quantity(symbol_info, qty: int):
    """Ensure quantity is a multiple of lot size."""
    lot_size = symbol_info["lot_size"]
    if qty % lot_size != 0:
        print(
            f"⚠️ Quantity {qty} is not a multiple of lot size {lot_size}. Adjusting...")
        qty = (qty // lot_size) * lot_size
    return qty
