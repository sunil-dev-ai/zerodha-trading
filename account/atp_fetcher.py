import requests
from account.symbol_manager import get_trade_config


def get_atp(symbol: str, exchange: str = "NSE"):
    """
    Fetch Average Traded Price (ATP) using NSE India API.
    Falls back to manual input if market is closed or API fails.
    """
    url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://www.nseindia.com/"
    }
    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=5)
        data = response.json()
        # NSE API provides ATP in priceInfo.averagePrice
        return data["priceInfo"]["averagePrice"]
    except Exception as e:
        print(f"❌ API call failed: {str(e)}")
        return float(input(f"Enter current ATP for {symbol}: ").strip())


if __name__ == "__main__":
    trade_config = get_trade_config()
    symbol = trade_config["SYMBOL"]
    atp = get_atp(symbol)
    print(f"✅ Average Traded Price (ATP) of {symbol}: {atp}")
