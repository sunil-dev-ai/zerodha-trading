# core/cancel_order.py

from core.kite_client import kite, set_access_token


def cancel_order(order_id: str):
    """
    Cancel an OPEN/PENDING regular order.

    Returns True if cancelled.
    """

    try:

        set_access_token()

        orders = kite.orders()

        for order in orders:

            if order["order_id"] == order_id:

                if order["status"] == "COMPLETE":

                    print("⚠ Order already executed.")

                    return False

                if order["status"] == "CANCELLED":

                    print("⚠ Order already cancelled.")

                    return False

                kite.cancel_order(
                    variety=order["variety"],
                    order_id=order_id
                )

                print(f"✅ Order Cancelled : {order_id}")

                return True

        print("❌ Order not found.")

        return False

    except Exception as e:

        print(f"❌ Failed to cancel order : {e}")

        return False


if __name__ == "__main__":

    order_id = input("Enter Order ID : ")

    cancel_order(order_id)
