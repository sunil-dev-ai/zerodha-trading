# account/volume_fetcher.py

import yfinance as yf


def get_volume_strength(
    symbol: str,
    exchange: str = "NSE",
    average_days: int = 20,
):

    """
    Returns volume strength.

    Example:
    {
        "symbol": "RELIANCE",
        "volume": 2500000,
        "average_volume": 1800000,
        "strength": True
    }
    """

    suffix = ".NS" if exchange.upper() == "NSE" else ".BO"

    ticker = f"{symbol}{suffix}"

    try:

        stock = yf.Ticker(ticker)

        # Daily candles for volume analysis
        df = stock.history(
            period="3mo",
            interval="1d",
            auto_adjust=False,
        )


        if df.empty:

            raise ValueError(
                "No volume data returned"
            )


        current_volume = int(
            df["Volume"].iloc[-1]
        )


        average_volume = int(
            df["Volume"]
            .tail(average_days)
            .mean()
        )


        strength = (
            current_volume > average_volume
        )


        return {

            "symbol": symbol,

            "volume": current_volume,

            "average_volume": average_volume,

            "strength": strength

        }


    except Exception as e:

        print(
            f"❌ Volume Error {symbol}: {e}"
        )

        return None



if __name__ == "__main__":

    result = get_volume_strength(
        "RELIANCE"
    )

    print(result)
