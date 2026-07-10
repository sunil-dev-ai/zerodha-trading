import pandas as pd
import pandas_ta as ta
import yfinance as yf

from account.symbol_manager import get_trade_config


def get_supertrend(
    symbol: str,
    exchange: str = "NSE",
    interval: str = "1m",
    period: int = 10,
    multiplier: float = 3.0,
):
    """
    Returns the latest Supertrend data.

    Example:
    {
        "symbol": "TATASTEEL",
        "close": 187.25,
        "supertrend": 187.49,
        "signal": "SELL"
    }
    """

    suffix = ".NS" if exchange.upper() == "NSE" else ".BO"
    ticker = f"{symbol}{suffix}"

    try:
        stock = yf.Ticker(ticker)

        df = stock.history(
            period="5d",
            interval=interval,
            auto_adjust=False,
        )

        if df.empty:
            raise ValueError("No historical data returned.")

        st = ta.supertrend(
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            length=period,
            multiplier=multiplier,
        )

        df = pd.concat([df, st], axis=1)

        latest = df.iloc[-1]

        return {
            "symbol": symbol,
            "close": round(float(latest["Close"]), 2),
            "supertrend": round(
                float(latest[f"SUPERT_{period}_{multiplier}"]), 2
            ),
            "signal": (
                "BUY"
                if latest[f"SUPERTd_{period}_{multiplier}"] == 1
                else "SELL"
            ),
        }

    except Exception as e:
        print(f"❌ Error fetching Supertrend: {e}")
        return None


if __name__ == "__main__":
    trade_config = get_trade_config()

    result = get_supertrend(
        symbol=trade_config["SYMBOL"],
        exchange=trade_config.get("EXCHANGE", "NSE"),
    )

    if result:
        print(
            f"{result['symbol']} | "
            f"Close: ₹{result['close']:.2f} | "
            f"Supertrend: ₹{result['supertrend']:.2f} | "
            f"Signal: {result['signal']}"
        )
