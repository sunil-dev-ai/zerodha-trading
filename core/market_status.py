# market_status.py

from datetime import datetime, time
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

MARKET_OPEN = time(9, 30)
MARKET_CLOSE = time(15, 30)


def get_market_status():
    """
    Returns:
    {
        "live": bool,
        "remaining_minutes": int
    }
    """

    now = datetime.now(IST)

    # Weekend
    if now.weekday() >= 5:
        return {
            "live": False,
            "remaining_minutes": 0
        }

    # Before market opens
    if now.time() < MARKET_OPEN:
        return {
            "live": False,
            "remaining_minutes": 0
        }

    # After market closes
    if now.time() > MARKET_CLOSE:
        return {
            "live": False,
            "remaining_minutes": 0
        }

    market_close = datetime.combine(
        now.date(),
        MARKET_CLOSE,
        tzinfo=IST
    )

    remaining = int(
        (market_close - now).total_seconds() // 60
    )

    return {
        "live": True,
        "remaining_minutes": remaining
    }


if __name__ == "__main__":

    status = get_market_status()

    if status["live"]:
        print(f"✅ Market is LIVE")
        print(f"⏳ Remaining Time: {status['remaining_minutes']} minutes")
    else:
        print("❌ Market is CLOSED")