from core.kite_client import kite, set_access_token


def get_balance():
    """Fetch account balance (funds) from Zerodha Kite API."""
    set_access_token()
    funds = kite.margins("equity")
    return funds


if __name__ == "__main__":
    try:
        balance = get_balance()
        print("✅ Account Balance Details:")
        print(f"Opening Balance: {balance['available']['cash']:.2f}")
        print(f"Used Margin: {balance['utilised']['debits']:.2f}")
        print(f"Available Cash: {balance['net']:.2f}")
    except Exception as e:
        print("❌ Failed to fetch balance:", str(e))
