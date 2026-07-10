# account/rsi_fetcher.py

import pandas as pd
import pandas_ta as ta
import yfinance as yf


def get_rsi(
    symbol: str,
    exchange: str = "NSE",
    interval: str = "1m",
    length: int = 14,
):
    """
    Returns latest RSI data.

    Example:
    {
        "symbol": "INFY",
        "close": 1654.25,
        "rsi": 62.45,
        "trend": "STRONG"
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
            raise ValueError("No historical data returned")

        rsi = ta.rsi(
            df["Close"],
            length=length,
        )

        df["RSI"] = rsi

        latest = df.iloc[-1]

        rsi_value = float(latest["RSI"])

        if rsi_value >= 70:
            trend = "OVERBOUGHT"

        elif rsi_value >= 55:
            trend = "STRONG"

        elif rsi_value >= 45:
            trend = "NEUTRAL"

        else:
            trend = "WEAK"


        return {

            "symbol": symbol,

            "close": round(
                float(latest["Close"]),
                2
            ),

            "rsi": round(
                rsi_value,
                2
            ),

            "trend": trend
        }


    except Exception as e:

        print(
            f"❌ RSI Error {symbol}: {e}"
        )

        return None



if __name__ == "__main__":

    result = get_rsi(
        "RELIANCE"
    )

    print(result)
