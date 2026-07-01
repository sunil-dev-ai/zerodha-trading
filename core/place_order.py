# core/place_order.py

from core.kite_client import kite, set_access_token
from core.instrument_helper import get_option_symbol, validate_quantity


def place_order(symbol: str, quantity: int, transaction_type: str = "BUY",
                exchange: str = "NSE", product: str = "CNC",
                order_type: str = "LIMIT", price: float = None):
    """Place a regular order (buy/sell)."""
    try:
        set_access_token()
        order_id = kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange=exchange,
            tradingsymbol=symbol,
            transaction_type=transaction_type,
            quantity=quantity,
            product=product,
            order_type=order_type,
            price=price if order_type == kite.ORDER_TYPE_LIMIT else None
        )
        print(
            f"✅ {transaction_type} order placed successfully! Order ID: {order_id}")
        return order_id
    except Exception as e:
        print(f"❌ Failed to place {transaction_type} order: {str(e)}")
        return None


def place_gtt_single(symbol: str, quantity: int, transaction_type: str = "BUY",
                     exchange: str = "NSE", trigger_price: float = None,
                     price: float = None, product: str = "CNC"):
    """Place a single-leg GTT order."""
    try:
        set_access_token()
        order_id = kite.place_gtt(
            trigger_type=kite.GTT_TYPE_SINGLE,
            exchange=exchange,
            tradingsymbol=symbol,
            trigger_values=[trigger_price],
            last_price=price,
            orders=[{
                "transaction_type": transaction_type,
                "quantity": quantity,
                "price": price,
                "product": product,
                "order_type": kite.ORDER_TYPE_LIMIT
            }]
        )
        print(
            f"✅ {transaction_type} Single GTT order placed successfully! Order ID: {order_id}")
        return order_id
    except Exception as e:
        print(
            f"❌ Failed to place {transaction_type} Single GTT order: {str(e)}")
        return None


def place_gtt_oco(symbol: str, quantity: int, exchange: str = "NSE",
                  target_trigger: float = None, target_price: float = None,
                  stop_trigger: float = None, stop_price: float = None,
                  product: str = "CNC"):
    """Place an OCO (One Cancels Other) GTT order."""
    try:
        set_access_token()
        order_id = kite.place_gtt(
            trigger_type=kite.GTT_TYPE_OCO,
            exchange=exchange,
            tradingsymbol=symbol,
            trigger_values=[target_trigger, stop_trigger],
            last_price=stop_price,
            orders=[
                {
                    "transaction_type": kite.TRANSACTION_TYPE_SELL,
                    "quantity": quantity,
                    "price": target_price,
                    "product": product,
                    "order_type": kite.ORDER_TYPE_LIMIT
                },
                {
                    "transaction_type": kite.TRANSACTION_TYPE_SELL,
                    "quantity": quantity,
                    "price": stop_price,
                    "product": product,
                    "order_type": kite.ORDER_TYPE_LIMIT
                }
            ]
        )
        print(
            f"✅ SELL OCO GTT order placed successfully! Order ID: {order_id}")
        return order_id
    except Exception as e:
        print(f"❌ Failed to place SELL OCO GTT order: {str(e)}")
        return None


if __name__ == "__main__":
    print("Choose instrument type:")
    print("1. Equity")
    print("2. F&O (Options/Futures)")
    inst_choice = input("Enter choice (1/2): ").strip()

    if inst_choice == "1":
        # Equity flow
        symbol = input(
            "Enter equity symbol (e.g., INFY, RELIANCE): ").strip().upper()
        qty = int(input("Enter quantity: ").strip())

    else:
        # F&O flow
        underlying = input(
            "Enter underlying (e.g., NIFTY, BANKNIFTY): ").strip().upper()
        strike = int(input("Enter strike price (e.g., 23950): ").strip())
        opt_type = input("Enter option type (CE/PE): ").strip().upper()
        expiry = input(
            "Enter expiry (YYYY-MM-DD / current week / monthly): ").strip()

        contract = get_option_symbol(underlying, strike, opt_type, expiry)
        if not contract:
            print("❌ Contract not found. Please check expiry/strike.")
            exit()

        symbol = contract["tradingsymbol"]
        qty = int(input("Enter quantity: ").strip())
        qty = validate_quantity(contract, qty)  # auto-adjust lot size

    action = input("Enter action (BUY/SELL): ").strip().upper()

    print("\nChoose order mode:")
    print("1. Regular Order")
    print("2. Single GTT Order")
    print("3. OCO GTT Order (target + stop-loss)")
    mode_choice = input("Enter choice (1/2/3): ").strip()

    # Product type selection
    print("\nChoose product type:")
    print("1. CNC (Delivery for equities)")
    print("2. MIS (Intraday)")
    print("3. NRML (Derivatives)")
    product_choice = input("Enter choice (1/2/3): ").strip()
    product_map = {"1": kite.PRODUCT_CNC,
                   "2": kite.PRODUCT_MIS, "3": kite.PRODUCT_NRML}
    product = product_map.get(product_choice, kite.PRODUCT_CNC)

    if mode_choice == "1":
        print("\nChoose order type:")
        print("1. LIMIT (specify price)")
        print("2. MARKET")
        order_choice = input("Enter choice (1/2): ").strip()

        if order_choice == "1":
            order_type = kite.ORDER_TYPE_LIMIT
            price = float(input("Enter limit price: ").strip())
        else:
            order_type = kite.ORDER_TYPE_MARKET
            price = None

        place_order(symbol, qty, transaction_type=action,
                    product=product, order_type=order_type, price=price)

    elif mode_choice == "2":
        trigger_price = float(input("Enter trigger price: ").strip())
        limit_price = float(input("Enter limit price: ").strip())
        place_gtt_single(symbol, qty, transaction_type=action,
                         product=product, trigger_price=trigger_price, price=limit_price)

    else:
        print("\nEnter target and stop-loss details:")
        target_trigger = float(input("Enter target trigger price: ").strip())
        target_price = float(input("Enter target limit price: ").strip())
        stop_trigger = float(input("Enter stop-loss trigger price: ").strip())
        stop_price = float(input("Enter stop-loss limit price: ").strip())

        place_gtt_oco(symbol, qty, product=product,
                      target_trigger=target_trigger, target_price=target_price,
                      stop_trigger=stop_trigger, stop_price=stop_price)
