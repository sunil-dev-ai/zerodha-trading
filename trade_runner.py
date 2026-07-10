# trade_runner.py

from strategy.strategy_v1 import run_strategy


def main():

    print("""
============================================================
              BLUECHIP TRADING BOT
              Strategy Version : V1
============================================================
""")

    print(
        "🚀 Starting Trading Strategy..."
    )


    try:
        
        run_strategy()


    except KeyboardInterrupt:

        print(
            """
============================================================
🛑 Trading Bot Stopped Manually
============================================================
"""
        )


    except Exception as e:

        print(
            """
============================================================
❌ TRADING BOT ERROR
============================================================
"""
        )

        print(
            str(e)
        )


if __name__ == "__main__":

    main()
