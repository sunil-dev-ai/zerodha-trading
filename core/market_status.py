from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

MARKET_OPEN = time(9, 15)
MARKET_CLOSE = time(15, 30)


def get_market_status():
    now = datetime.now(IST)

    # Weekend
    if now.weekday() >= 5:
        days = 7 - now.weekday()  # Saturday->2, Sunday->1
        next_open = datetime.combine(
            now.date() + timedelta(days=days),
            MARKET_OPEN,
            tzinfo=IST,
        )

        remaining = int((next_open - now).total_seconds() // 60)

        return {
            "live": False,
            "remaining_minutes": remaining,
        }

    today_open = datetime.combine(now.date(), MARKET_OPEN, tzinfo=IST)
    today_close = datetime.combine(now.date(), MARKET_CLOSE, tzinfo=IST)

    # Before market opens
    if now < today_open:
        remaining = int((today_open - now).total_seconds() // 60)

        return {
            "live": False,
            "remaining_minutes": remaining,
        }

    # After market closes
    if now > today_close:
        next_day = now.date() + timedelta(days=1)

        # Skip weekend
        while next_day.weekday() >= 5:
            next_day += timedelta(days=1)

        next_open = datetime.combine(next_day, MARKET_OPEN, tzinfo=IST)

        remaining = int((next_open - now).total_seconds() // 60)

        return {
            "live": False,
            "remaining_minutes": remaining,
        }

    # Market is live
    remaining = int((today_close - now).total_seconds() // 60)

    return {
        "live": True,
        "remaining_minutes": remaining,
    }

if __name__ == "__main__":

    status = get_market_status()

    if status["live"]:
        print(f"✅ Market is LIVE")
        print(f"⏳ Remaining Time: {status['remaining_minutes']} minutes")
    else:
        print("❌ Market is CLOSED")