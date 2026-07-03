import requests
from account.symbol_manager import get_trade_config


def get_ltp(symbol: str, exchange: str = "NSE"):
    """
    Fetch LTP using Yahoo Finance API.
    Falls back to previous close or manual input if market is closed.
    """
    suffix = ".NS" if exchange.upper() == "NSE" else ".BO"
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}{suffix}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        result = data["quoteResponse"]["result"]
        if not result:
            raise ValueError("Empty response (market closed)")
        quote = result[0]
        # Prefer live price, fallback to previous close
        return quote.get("regularMarketPrice") or quote.get("regularMarketPreviousClose")
    except Exception as e:
        print(f"❌ API call failed: {str(e)}")
        return float(input(f"Enter current LTP for {symbol}: ").strip())


if __name__ == "__main__":
    trade_config = get_trade_config()
    symbol = trade_config["SYMBOL"]
    ltp = get_ltp(symbol)
    print(f"✅ Current LTP of {symbol}: {ltp}")
