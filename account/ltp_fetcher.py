import yfinance as yf
from account.symbol_manager import get_trade_config


def get_ltp(symbol: str, exchange: str = "NSE"):
    """
    Fetch LTP (Last Traded Price) using yfinance.
    Works for both NSE (.NS) and BSE (.BO).
    """
    suffix = ".NS" if exchange.upper() == "NSE" else ".BO"
    try:
        stock = yf.Ticker(symbol + suffix)
        data = stock.history(period="1d")
        if data.empty:
            raise ValueError("No data returned for symbol")
        # Use the latest close price as LTP
        return float(data["Close"].iloc[-1])
    except Exception as e:
        print(f"❌ API call failed: {str(e)}")
        return None


if __name__ == "__main__":
    trade_config = get_trade_config()
    symbol = trade_config["SYMBOL"]
    ltp = get_ltp(symbol)
    if ltp:
        # Format to 2 decimal places
        print(f"✅ Last Traded Price (LTP) of {symbol}: {ltp:.2f}")
    else:
        print(f"❌ Could not fetch LTP for {symbol}")
