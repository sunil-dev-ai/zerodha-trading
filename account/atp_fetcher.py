import yfinance as yf
from account.symbol_manager import get_trade_config


def get_atp(symbol: str, exchange: str = "NSE"):
    """
    Fetch Average Traded Price (ATP) using yfinance intraday data.
    Approximates ATP as VWAP (Volume Weighted Average Price).
    """
    suffix = ".NS" if exchange.upper() == "NSE" else ".BO"
    try:
        stock = yf.Ticker(symbol + suffix)
        # Fetch intraday data (1-minute interval for today)
        data = stock.history(period="1d", interval="1m")
        if data.empty:
            raise ValueError("No intraday data returned for symbol")

        # Calculate VWAP = sum(price * volume) / sum(volume)
        vwap = (data["Close"] * data["Volume"]).sum() / data["Volume"].sum()
        return float(vwap)
    except Exception as e:
        print(f"❌ API call failed: {str(e)}")
        return None


if __name__ == "__main__":
    trade_config = get_trade_config()
    symbol = trade_config["SYMBOL"]
    atp = get_atp(symbol)
    if atp:
        print(f"✅ Average Traded Price (ATP) of {symbol}: {atp:.2f}")
    else:
        print(f"❌ Could not fetch ATP for {symbol}")
