import time
from strategy.bluechip_strategy import run_bluechip_strategy
from core.place_order import place_order, kite
from account.ltp_fetcher import get_ltp
from account.atp_fetcher import get_atp
from utils.trade_logger import log_trade


def adjust_to_tick(price: float, tick_size: float) -> float:
    """Round price to nearest valid tick size multiple."""
    return round(round(price / tick_size) * tick_size, 2)


def get_tick_size(symbol: str, exchange: str = "NSE") -> float:
    """
    Fetch tick size dynamically from Kite instruments API.
    """
    instruments = kite.instruments(exchange=exchange)
    for inst in instruments:
        if inst["tradingsymbol"] == symbol:
            return inst["tick_size"]
    # Default fallback
    return 0.05


def main():
    candidate = run_bluechip_strategy()
    if not candidate:
        print("⚠️ No candidate selected. Exiting.")
        return

    print("\n➡️ Final Candidate Details:")
    print(candidate)

    symbol = candidate["symbol"]
    qty = candidate["quantity"]
    ltp = candidate["ltp"]
    target_price = candidate["target_price"]

    # Step 1: Place regular BUY order at LTP
    buy_order_id = place_order(
        symbol=symbol,
        quantity=qty,
        transaction_type="BUY",
        order_type=kite.ORDER_TYPE_LIMIT,
        price=ltp,
        product=kite.PRODUCT_CNC
    )

    if not buy_order_id:
        print("❌ Failed to place BUY order.")
        return

    print(
        f"✅ BUY order placed for {symbol} at ₹{ltp:.2f}, Qty: {qty}, Order ID: {buy_order_id}")

    # Step 2: Monitor BUY order until execution
    executed = False
    while not executed:
        time.sleep(5)
        current_ltp = get_ltp(symbol)
        current_atp = get_atp(symbol)

        if current_ltp is not None and current_atp is not None:
            print(
                f"Monitoring BUY... LTP: ₹{current_ltp:.2f}, ATP: ₹{current_atp:.2f}")
        else:
            print("⚠️ LTP/ATP data not available, retrying...")
            continue

        if current_ltp < current_atp:
            print("⚠️ LTP fell below ATP. Cancelling BUY order.")
            kite.cancel_order(order_id=buy_order_id,
                              variety=kite.VARIETY_REGULAR)
            return

        if abs(current_ltp - ltp) < 0.01:
            executed = True
            print(f"✅ BUY order executed for {symbol} at ₹{ltp:.2f}")

    # Step 3: Place SELL order at target price (adjusted to tick size)
    tick_size = get_tick_size(symbol)
    valid_target_price = adjust_to_tick(target_price, tick_size)

    sell_order_id = place_order(
        symbol=symbol,
        quantity=qty,
        transaction_type="SELL",
        order_type=kite.ORDER_TYPE_LIMIT,
        price=valid_target_price,
        product=kite.PRODUCT_CNC
    )

    if not sell_order_id:
        print("❌ Failed to place SELL order.")
        return

    print(
        f"✅ SELL order placed for {symbol} at ₹{valid_target_price:.2f}, Qty: {qty}, Order ID: {sell_order_id}")

    # Step 4: Monitor SELL execution
    sell_executed = False
    while not sell_executed:
        time.sleep(5)
        current_ltp = get_ltp(symbol)

        if current_ltp is not None:
            print(f"Monitoring SELL... LTP: ₹{current_ltp:.2f}")
        else:
            print("⚠️ LTP data not available, retrying...")
            continue

        if current_ltp >= valid_target_price:
            sell_executed = True
            print(
                f"✅ SELL order executed for {symbol} at ₹{valid_target_price:.2f}")
            profit = (valid_target_price - ltp) * qty
            print(
                f"🎉 Congratulations! You achieved your goal with a profit of ₹{profit:.2f}")
            log_trade(symbol, qty, ltp, valid_target_price, profit)


if __name__ == "__main__":
    main()
