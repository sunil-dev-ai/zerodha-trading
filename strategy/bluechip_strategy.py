# strategy/bluechip_strategy.py

import os

from account.quantity_calculator import calculate_quantity
from account.balance_checker import get_balance
from account.atp_fetcher import get_atp


# =====================================================
# CONFIG PATH
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

CONFIG_FILE = os.path.join(
    BASE_DIR,
    "config",
    "trade_config.txt"
)



# =====================================================
# LOAD CONFIG
# =====================================================

def load_config(config_file=CONFIG_FILE):

    config = {}

    try:

        with open(
            config_file,
            "r"
        ) as file:

            for line in file:

                line = line.strip()

                if (
                    not line
                    or "=" not in line
                    or line.startswith("#")
                ):
                    continue


                key, value = line.split(
                    "=",
                    1
                )

                config[key.strip()] = value.strip()


    except FileNotFoundError:

        print(
            "❌ trade_config.txt not found"
        )


    return config



# =====================================================
# LOAD STOCK SECTION
# =====================================================

def load_section(
        section_name,
        config_file=CONFIG_FILE
):

    stocks = []

    try:

        with open(
            config_file,
            "r"
        ) as file:

            lines = file.readlines()


        capture = False


        for line in lines:

            line = line.strip()


            if line == section_name:

                capture = True
                continue



            if capture:

                if (
                    line.startswith("--")
                    or not line
                ):

                    break


                if "," in line:

                    stocks.extend(
                        [
                            x.strip().upper()
                            for x in line.split(",")
                        ]
                    )

                else:

                    stocks.append(
                        line.upper()
                    )


    except FileNotFoundError:

        print(
            "❌ trade_config.txt missing"
        )


    return stocks




# =====================================================
# BLUECHIP SCANNER
# =====================================================

def run_bluechip_strategy():

    """
    Scan all bluechip stocks.

    Returns:

    {
        selected_stocks: [],
        best_candidate: {}
    }

    """


    balance = get_balance()

    available_margin = balance["net"]



    stocks = load_section(
        "--BLUECHIP_STOCKS--"
    )


    if not stocks:

        print(
            "❌ No BLUECHIP_STOCKS found"
        )

        return None



    print(
        "\n✅ Running Bluechip Strategy"
    )

    print(
        f"Available Margin : ₹{available_margin:.2f}"
    )

    print(
        f"Scanning Stocks  : {len(stocks)}\n"
    )



    crossed_candidates = []

    fallback_candidates = []



    for symbol in stocks:


        qty, ltp = calculate_quantity(
            symbol,
            available_margin
        )



        if not ltp:

            print(
                f"❌ LTP unavailable {symbol}"
            )

            continue
        
        if qty < 1:

            print(
                f"❌ Insufficient margin for {symbol} | Qty: {qty}"
            )

            continue



        atp = get_atp(
            symbol
        )



        print(
            "-" * 50
        )

        print(
            f"Symbol   : {symbol}"
        )

        print(
            f"LTP      : ₹{ltp:.2f}"
        )

        print(
            f"Quantity : {qty}"
        )



        if atp:


            strength = (
                (ltp - atp)
                /
                atp
            ) * 100



            crossed = (
                ltp > atp
            )



            print(
                f"ATP      : ₹{atp:.2f}"
            )

            print(
                f"Strength : {strength:.2f}%"
            )


            print(
                "Status   : "
                +
                (
                    "ATP BREAKOUT"
                    if crossed
                    else
                    "Below ATP"
                )
            )



            candidate = {

                "symbol": symbol,

                "ltp": round(
                    ltp,
                    2
                ),

                "quantity": qty,

                "atp": round(
                    atp,
                    2
                ),

                "strength": round(
                    strength,
                    2
                )

            }



            if crossed:

                crossed_candidates.append(
                    candidate
                )

            else:

                fallback_candidates.append(
                    candidate
                )



        else:


            print(
                "ATP : N/A"
            )


            fallback_candidates.append(

                {

                    "symbol": symbol,

                    "ltp": round(
                        ltp,
                        2
                    ),

                    "quantity": qty,

                    "atp": None,

                    "strength": 0

                }

            )




    # =================================================
    # FINAL SELECTION
    # =================================================


    if crossed_candidates:


        crossed_candidates.sort(

            key=lambda x:
                x["strength"],

            reverse=True

        )


        best_candidate = next(
            (
                x for x in crossed_candidates
                if x["quantity"] >= 1
            ),
            None
        )


        if not best_candidate:
            print(
                "❌ No ATP breakout candidate with valid quantity"
            )
            return None

        print(
            "\n🎯 BEST ATP BREAKOUT"
        )

        print(
            best_candidate
        )

        return {

            "selected_stocks":
                crossed_candidates,

            "best_candidate":
                best_candidate

        }



    elif fallback_candidates:

        best_candidate = next(
            (
                x for x in fallback_candidates
                if x["quantity"] >= 1
            ),
            None
        )


        if not best_candidate:
            print(
                "❌ No fallback candidate with valid quantity"
            )
            return None


        print(
            "\n⚠ No ATP breakout found"
        )

        print(
            "Fallback candidate:"
        )

        print(
            best_candidate
        )



        return {

            "selected_stocks":
                fallback_candidates,

            "best_candidate":
                best_candidate

        }



    else:


        print(
            "❌ No candidates found"
        )

        return None





# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":


    result = run_bluechip_strategy()


    if result:

        print(
            "\nFINAL RESULT"
        )

        print(
            result
        )
