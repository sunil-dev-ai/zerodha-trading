# core/order_status.py

from core.kite_client import kite, set_access_token


def get_order_status(order_id: str):
    """
    Fetch order status.

    Returns:
    {
        "order_id": "...",
        "status": "OPEN",
        "filled_quantity": 0,
        "pending_quantity": 10,
        "average_price": 0.0,
        "tradingsymbol": "INFY"
    }

    Returns None if order not found.
    """

    try:
        set_access_token()

        orders = kite.orders()

        for order in orders:

            if order["order_id"] == order_id:

                return {
                    "order_id": order["order_id"],
                    "status": order["status"],
                    "filled_quantity": order["filled_quantity"],
                    "pending_quantity": order["pending_quantity"],
                    "average_price": order["average_price"],
                    "tradingsymbol": order["tradingsymbol"],
                    "transaction_type": order["transaction_type"],
                    "quantity": order["quantity"],
                    "exchange": order["exchange"],
                    "order_type": order["order_type"],
                    "product": order["product"]
                }

        print(f"❌ Order {order_id} not found.")

        return None

    except Exception as e:

        print(f"❌ Failed to fetch order status: {e}")

        return None


if __name__ == "__main__":

    order_id = input("Enter Order ID : ")

    result = get_order_status(order_id)

    if result:

        print("\n========== ORDER STATUS ==========")

        for k, v in result.items():
            print(f"{k:20}: {v}")

        print("==================================")
