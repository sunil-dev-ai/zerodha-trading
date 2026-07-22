# strategy/strategy_v1.py

import time

from account.ltp_fetcher import get_ltp
from account.atp_fetcher import get_atp
from account.supertrend_fetcher import get_supertrend
from account.tick_size_fetcher import get_tick_size

from account.quantity_calculator import calculate_quantity
from account.balance_checker import get_balance
from account.macd_fetcher import get_macd

from core.place_order import place_order, kite
from core.order_status import get_order_status
from core.cancel_order import cancel_order
from core.market_status import get_market_status

from strategy.bluechip_strategy import run_bluechip_strategy

from utils.trade_logger import log_trade
from utils.price_utils import format_price


CHECK_INTERVAL = 10


def print_header(title):

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)



def print_line():

    print("-" * 60)



def get_market_data(symbol):

    """
    Always fetch fresh market data
    """

    ltp = get_ltp(symbol)

    atp = get_atp(symbol)

    supertrend = get_supertrend(symbol)
    
    macd = get_macd(symbol)

    return ltp, atp, supertrend, macd



# ============================================================
# BUY ORDER
# ============================================================

def place_buy(symbol, qty, ltp):

    tick_size = get_tick_size(symbol)

    buy_price = format_price(
        ltp,
        tick_size
    )

    print_header("BUY ORDER")

    print(f"Symbol      : {symbol}")
    print(f"Tick Size   : {tick_size}")
    print(f"Raw Price   : {ltp}")
    print(f"Order Price : {buy_price}")

    order_id = place_order(
        symbol=symbol,
        quantity=qty,
        transaction_type="BUY",
        exchange="NSE",
        product=kite.PRODUCT_CNC,
        order_type=kite.ORDER_TYPE_LIMIT,
        price=buy_price
    )


    if order_id:

        print(
            f"✅ BUY Order ID : {order_id}"
        )


    return order_id





def track_buy_order(symbol, order_id):


    print_header(
        "TRACKING BUY ORDER"
    )


    while True:


        time.sleep(CHECK_INTERVAL)


        ltp = get_ltp(symbol)

        atp = get_atp(symbol)

        trend = get_supertrend(symbol)


        status = get_order_status(order_id)



        if not status:

            print(
                "❌ Unable to fetch BUY order status"
            )

            return None



        print_line()


        print(
            f"LTP          : ₹{ltp:.2f}"
        )

        print(
            f"ATP          : ₹{atp:.2f}"
        )


        if trend:

            print(
                f"SuperTrend   : {trend['signal']}"
            )


        print(
            f"Order Status : {status['status']}"
        )


        print_line()




        if status["status"] == "COMPLETE":


            buy_price = status["average_price"]


            print_header(
                "BUY EXECUTED"
            )


            print(
                f"Buy Price : ₹{buy_price:.2f}"
            )


            print(
                f"Quantity  : {status['filled_quantity']}"
            )


            return {

                "buy_price": buy_price,

                "quantity": status["filled_quantity"]

            }





        if status["status"] in [

            "CANCELLED",

            "REJECTED"

        ]:

            print(
                "❌ BUY ORDER CLOSED"
            )

            return None




        # Cancel condition 1

        if ltp < atp:


            print(
                "\n⚠ LTP below ATP"
            )


            cancel_order(order_id)


            return None




        # Cancel condition 2

        if trend and trend["signal"] == "SELL":


            print(
                "\n⚠ SuperTrend changed SELL"
            )


            cancel_order(order_id)


            return None






# ============================================================
# POSITION TRACKING
# ============================================================

def track_position(symbol, qty):


    print_header(
        "POSITION TRACKING"
    )


    while True:


        time.sleep(CHECK_INTERVAL)



        ltp = get_ltp(symbol)

        atp = get_atp(symbol)

        trend = get_supertrend(symbol)



        print_line()


        print(
            f"LTP        : ₹{ltp:.2f}"
        )


        print(
            f"ATP        : ₹{atp:.2f}"
        )


        print(
            f"SuperTrend : {trend['signal']}"
        )


        print_line()



        status = get_market_status()

        if trend["signal"] == "SELL" or status["remaining_minutes"] <= 5:


            print_header(
                "SELL SIGNAL RECEIVED"
            )


            sell_order_id = place_order(

                symbol=symbol,

                quantity=qty,

                transaction_type="SELL",

                exchange="NSE",

                product=kite.PRODUCT_CNC,

                order_type=kite.ORDER_TYPE_MARKET

            )


            if sell_order_id:


                print(
                    f"✅ SELL Order ID : {sell_order_id}"
                )


                return sell_order_id





# ============================================================
# SELL TRACKING
# ============================================================

def track_sell_order(

        order_id,

        symbol,

        qty,

        buy_price

):


    print_header(
        "TRACKING SELL ORDER"
    )



    while True:


        time.sleep(CHECK_INTERVAL)



        status = get_order_status(order_id)



        if not status:

            print(
                "❌ Unable to fetch SELL status"
            )

            return




        print_line()


        print(
            f"SELL Status : {status['status']}"
        )


        print_line()




        if status["status"] == "COMPLETE":


            sell_price = status["average_price"]



            profit = (

                sell_price - buy_price

            ) * qty




            print_header(
                "🎉 TRADE COMPLETED"
            )




            if profit > 0:


                print(
"""
╔══════════════════════════════════════════╗
║                                          ║
║        🎊 CONGRATULATIONS BINGO!! 🎊     ║
║                                          ║
╚══════════════════════════════════════════╝
"""
                )


                print(
                    f"✅ Profit Booked : ₹{profit:.2f}"
                )


            else:


                print(
                    f"⚠ Loss : ₹{profit:.2f}"
                )




            print(
f"""
Symbol       : {symbol}

Quantity     : {qty}

Buy Price    : ₹{buy_price:.2f}

Sell Price   : ₹{sell_price:.2f}

Net Profit   : ₹{profit:.2f}
"""
            )



            log_trade(

                symbol,

                qty,

                buy_price,

                sell_price,

                profit

            )


            return




# ============================================================
# MAIN STRATEGY
# ============================================================

def run_strategy():


    strategy_result  = run_bluechip_strategy()


    symbol = strategy_result["best_candidate"]["symbol"]



    print_header(
        "BLUECHIP STRATEGY V1 STARTED"
    )



    balance = get_balance()



    print(
        f"Available Balance : ₹{balance['net']:.2f}"
    )
    
    print(
        f"Selected Share Symbol  : {symbol}"
    )




    while True:

        # ==========================================
        # MARKET CLOSE PROTECTION
        # ==========================================

        status = get_market_status()


        if status["remaining_minutes"] <= 5:

            print(
                "\n⏰ Market closing soon. No new trades allowed."
            )

            break

        print_header(
            "SCANNING MARKET"
        )



        ltp, atp, trend, macd = get_market_data(symbol)



        if not ltp or not atp or not trend or not macd:


            print(
                "❌ Market data unavailable"
            )


            time.sleep(CHECK_INTERVAL)

            continue





        print(
            f"Symbol      : {symbol}"
        )

        print(
            f"LTP         : ₹{ltp:.2f}"
        )


        print(
            f"ATP         : ₹{atp:.2f}"
        )


        print(
            f"Super Trend  : {trend['signal']}"
        )
        
        print(
            f"MACD Trend  : {macd['trend']}"
        )





        if (
            ltp > atp
            and trend["signal"] == "BUY"
            and macd["trend"] == "UPTREND"
            ):



            print(
                "\n✅ BUY CONDITION MATCHED"
            )



            qty, _ = calculate_quantity(

                symbol,

                balance["net"]

            )

            buy_order_id = place_buy(

                symbol,

                qty,

                ltp

            )



            if not buy_order_id:


                continue




            buy_result = track_buy_order(

                symbol,

                buy_order_id

            )



            if buy_result:



                sell_order_id = track_position(

                    symbol,

                    buy_result["quantity"]

                )



                track_sell_order(

                    sell_order_id,

                    symbol,

                    buy_result["quantity"],

                    buy_result["buy_price"]

                )




        else:


            print(
                "Waiting for BUY setup..."
            )



        time.sleep(CHECK_INTERVAL)



if __name__ == "__main__":


    try:

        run_strategy()


    except KeyboardInterrupt:


        print(
            "\n🛑 Strategy stopped manually"
        )


    except Exception as e:


        print(
            f"\n❌ Strategy Error : {e}"
        )
