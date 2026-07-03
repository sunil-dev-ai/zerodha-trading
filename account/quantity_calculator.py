from account.balance_checker import get_balance
from account.ltp_fetcher import get_ltp
from account.atp_fetcher import get_atp
from account.symbol_manager import get_trade_config


def calculate_quantity(symbol: str, available_margin: float, exchange: str = "NSE"):
    """
    Calculate maximum purchasable quantity based on available margin and LTP.
    Deducts a fixed buffer (₹50) for brokerage/charges.
    """
    ltp = get_ltp(symbol, exchange)
    if not ltp or ltp <= 0:
        print("❌ Invalid LTP, cannot calculate quantity.")
        return 0, ltp

    effective_margin = max(available_margin - 50, 0)
    quantity = int(effective_margin // ltp)
    return quantity, ltp


def evaluate_trade(trade_config: dict):
    """
    Use rupee values directly from config for expected profit and max loss.
    """
    expected_profit = float(trade_config.get("EXPECTED_PROFIT", 0))
    max_loss = float(trade_config.get("MAX_LOSS", 0))

    risk_reward = None
    if expected_profit > 0 and max_loss > 0:
        risk_reward = expected_profit / max_loss

    return expected_profit, max_loss, risk_reward


if __name__ == "__main__":
    trade_config = get_trade_config()
    symbol = trade_config["SYMBOL"]

    balance = get_balance()
    available_margin = balance["net"]

    qty, ltp = calculate_quantity(symbol, available_margin)
    atp = get_atp(symbol)  # NEW: fetch Average Traded Price
    expected_profit, max_loss, risk_reward = evaluate_trade(trade_config)

    print("✅ Risk-Aware Quantity Calculator")
    print(f"Symbol: {symbol}")
    print(f"LTP (Last Traded Price): {ltp:.2f}")
    print(f"ATP (Average Traded Price): {atp:.2f}")
    print(f"Available Margin: {available_margin:.2f}")
    print(f"Max Purchasable Quantity (after ₹50 buffer): {qty}")
    print(f"Expected Profit: ₹{expected_profit:.2f}")
    print(f"Max Loss: ₹{max_loss:.2f}")
    if risk_reward is not None:
        print(f"Risk/Reward Ratio: {risk_reward:.2f}")
