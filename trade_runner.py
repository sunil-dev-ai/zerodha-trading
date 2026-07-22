import time

from strategy.strategy_v1 import run_strategy

from core.market_status import get_market_status

from account.instrument_cache import InstrumentCache
from account.virtual_contract_note import get_virtual_contract_note

from utils.update_bluechip_stocks import main as update_bluechip_stocks


def print_daily_summary():

    note = get_virtual_contract_note()

    gross_pnl = note.get("Gross P&L", 0)

    print("""
============================================================
                 TODAY'S TRADING SUMMARY
============================================================
""")

    print(f"""
+--------------------------------------------+
| Metric                         | Value      |
+--------------------------------------------+
| Today's Gross P&L              | ₹{gross_pnl:.2f} |
+--------------------------------------------+
""")

    if gross_pnl > 0:
        print("🟢 Day Result : PROFIT")
    elif gross_pnl < 0:
        print("🔴 Day Result : LOSS")
    else:
        print("⚪ Day Result : NO TRADE")

    print("""
============================================================
""")


def main():

    print("""
============================================================
              BLUECHIP TRADING BOT
              Strategy Version : V1
============================================================
""")

    print("📊 Loading Instruments...")
    InstrumentCache.load()
    print("✅ Instruments Loaded")

    print("\n⏳ Checking Market Status...")

    while True:

        status = get_market_status()

        if status["live"]:
            print("\n✅ Market is LIVE")
            print(
                f"⏳ Remaining Trading Time : {status['remaining_minutes']} minutes"
            )
            break

        print(
            f"\r❌ Market is CLOSED | Opens in {status['remaining_minutes']} minutes...",
            end="",
            flush=True
        )

        time.sleep(60)

    print("\n\n🔄 Updating Bluechip Stock List...")

    try:

        update_bluechip_stocks()

        print("✅ Bluechip stock list updated")

    except Exception as e:

        print("❌ Bluechip update failed")
        print(str(e))
        return

    print("\n🚀 Starting Trading Strategy...")

    try:

        run_strategy()
        print_daily_summary()

    except KeyboardInterrupt:

        print("""
============================================================
🛑 Trading Bot Stopped Manually
============================================================
""")

    except Exception as e:

        print("""
============================================================
❌ TRADING BOT ERROR
============================================================
""")

        print(str(e))


if __name__ == "__main__":
    main()