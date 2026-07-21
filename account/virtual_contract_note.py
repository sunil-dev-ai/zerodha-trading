from core.kite_client import kite, set_access_token



def get_virtual_contract_note(order_id=None):

    """
    Fetch virtual contract note data from Kite.

    If order_id is provided:
        Fetch that order trades only.

    If order_id is None:
        Fetch all completed orders of the day.
    """


    # Refresh Kite session
    set_access_token()


    trades = []

    successful_orders = set()



    # Fetch single order
    if order_id:


        order_trades = kite.order_trades(
            order_id
        )


        if order_trades:

            successful_orders.add(
                order_id
            )


        trades.extend(
            order_trades
        )



    # Fetch all completed orders
    else:


        orders = kite.orders()


        for order in orders:


            if order["status"] == "COMPLETE":


                successful_orders.add(
                    order["order_id"]
                )


                order_trades = kite.order_trades(
                    order["order_id"]
                )


                trades.extend(
                    order_trades
                )



    if not trades:

        return None



    total_quantity = 0

    total_turnover = 0


    buy_quantity = 0

    buy_value = 0


    sell_quantity = 0

    sell_value = 0



    for trade in trades:


        qty = trade["quantity"]

        price = trade["average_price"]

        value = qty * price



        total_quantity += qty

        total_turnover += value



        if trade["transaction_type"] == "BUY":


            buy_quantity += qty

            buy_value += value



        elif trade["transaction_type"] == "SELL":


            sell_quantity += qty

            sell_value += value




    gross_pnl = sell_value - buy_value



    return {


        "Successful Orders":
            len(successful_orders),


        "Total Trades":
            len(trades),


        "Symbol":
            trades[0]["tradingsymbol"],


        "Exchange":
            trades[0]["exchange"],


        "Total Quantity":
            total_quantity,


        "Total Turnover":
            round(
                total_turnover,
                2
            ),


        "BUY Quantity":
            buy_quantity,


        "BUY Value":
            round(
                buy_value,
                2
            ),


        "SELL Quantity":
            sell_quantity,


        "SELL Value":
            round(
                sell_value,
                2
            ),


        "Gross P&L":
            round(
                gross_pnl,
                2
            )

    }




if __name__ == "__main__":


    try:


        # Put order id here if required
        # Example:
        # order_id = "250721000123456"

        order_id = None



        note = get_virtual_contract_note(
            order_id
        )



        print("\n" + "=" * 60)

        print("VIRTUAL CONTRACT NOTE")

        print("=" * 60)



        if note:


            for key, value in note.items():

                print(
                    f"{key:<25}: {value}"
                )


        else:


            print(
                "No completed trades found"
            )



    except Exception as e:


        print(
            f"❌ Failed to fetch virtual contract note: {e}"
        )