import pandas as pd
import pandas_ta as ta
import yfinance as yf

from account.symbol_manager import get_trade_config


def get_macd(
    symbol: str,
    exchange: str = "NSE",
    interval: str = "1m",
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
):
    """
    Returns the latest MACD data.

    Example:
    {
        "symbol": "INFY",
        "close": 1654.25,
        "macd": 2.34,
        "signal_line": 1.98,
        "histogram": 0.36,
        "trend": "UPTREND"
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

        macd = ta.macd(
            close=df["Close"],
            fast=fast,
            slow=slow,
            signal=signal,
        )

        df = pd.concat([df, macd], axis=1)

        latest = df.iloc[-1]

        macd_value = float(latest[f"MACD_{fast}_{slow}_{signal}"])
        signal_value = float(latest[f"MACDs_{fast}_{slow}_{signal}"])
        histogram = float(latest[f"MACDh_{fast}_{slow}_{signal}"])

        trend = (
            "UPTREND"
            if macd_value > signal_value
            else "DOWNTREND"
        )

        return {
            "symbol": symbol,
            "close": round(float(latest["Close"]), 2),
            "macd": round(macd_value, 4),
            "signal_line": round(signal_value, 4),
            "histogram": round(histogram, 4),
            "trend": trend,
        }

    except Exception as e:
        print(f"❌ Error fetching MACD: {e}")
        return None


if __name__ == "__main__":

    trade_config = get_trade_config()

    result = get_macd(
        symbol=trade_config["SYMBOL"],
        exchange=trade_config.get("EXCHANGE", "NSE"),
    )

    if result:

        print(
            f"{result['symbol']} | "
            f"Close: ₹{result['close']:.2f} | "
            f"MACD: {result['macd']:.4f} | "
            f"Signal: {result['signal_line']:.4f} | "
            f"Histogram: {result['histogram']:.4f} | "
            f"Trend: {result['trend']}"
        )
