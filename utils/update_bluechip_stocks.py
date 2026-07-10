# utils/update_bluechip_stocks.py

import os
import pandas as pd
import requests
from io import StringIO


from config.settings import TRADE_CONFIG_FILE

from account.ltp_fetcher import get_ltp
from account.atp_fetcher import get_atp
from account.supertrend_fetcher import get_supertrend
from account.macd_fetcher import get_macd
from account.rsi_fetcher import get_rsi
from account.volume_fetcher import get_volume_strength


TOP_STOCKS = 10


NIFTY50_URL = (
    "https://archives.nseindia.com/"
    "content/indices/ind_nifty50list.csv"
)


HEADERS = {
    "User-Agent":
        "Mozilla/5.0"
}



# ======================================================
# FETCH NIFTY 50
# ======================================================

def fetch_nifty50():

    print("\nFetching NIFTY 50 list...")

    response = requests.get(
        NIFTY50_URL,
        headers=HEADERS,
        timeout=20
    )

    response.raise_for_status()

    df = pd.read_csv(
        StringIO(response.text)
    )

    symbols = (
        df["Symbol"]
        .dropna()
        .astype(str)
        .str.upper()
        .tolist()
    )

    print(
        f"NIFTY 50 stocks found : {len(symbols)}"
    )

    return symbols




# ======================================================
# STOCK SCORING
# ======================================================

def analyse_stock(symbol):

    score = 0

    result = {
        "symbol": symbol
    }


    print(
        f"\nScanning {symbol}"
    )


    # -------------------------
    # LTP / ATP
    # -------------------------

    try:

        ltp = get_ltp(symbol)

        atp = get_atp(symbol)


        if ltp:

            result["ltp"] = ltp


        if atp:

            result["atp"] = atp


        if ltp and atp:

            if ltp > atp:

                score += 30

    except Exception as e:

        print(
            f"LTP/ATP error {symbol}: {e}"
        )



    # -------------------------
    # SUPERTREND
    # -------------------------

    try:

        supertrend = get_supertrend(
            symbol
        )


        if supertrend:

            result["supertrend"] = (
                supertrend["signal"]
            )


            if (
                supertrend["signal"]
                == "BUY"
            ):

                score += 30


    except Exception as e:

        print(
            f"SuperTrend error {symbol}: {e}"
        )



    # -------------------------
    # MACD
    # -------------------------

    try:

        macd = get_macd(
            symbol
        )


        if macd:

            result["macd"] = (
                macd["trend"]
            )


            if (
                macd["trend"]
                == "UPTREND"
            ):

                score += 20


    except Exception as e:

        print(
            f"MACD error {symbol}: {e}"
        )



    # -------------------------
    # RSI
    # -------------------------

    try:

        rsi = get_rsi(
            symbol
        )


        if rsi:

            result["rsi"] = (
                rsi["rsi"]
            )


            if (
                55 <= rsi["rsi"] <= 70
            ):

                score += 10


    except Exception as e:

        print(
            f"RSI error {symbol}: {e}"
        )



    # -------------------------
    # VOLUME
    # -------------------------

    try:

        volume = get_volume_strength(
            symbol
        )


        if volume:

            result["volume"] = (
                volume["volume"]
            )


            if volume["strength"]:

                score += 10


    except Exception as e:

        print(
            f"Volume error {symbol}: {e}"
        )



    result["score"] = score


    print(
        f"{symbol} Score : {score}/100"
    )


    return result




# ======================================================
# UPDATE trade_config.txt
# ======================================================

def update_trade_config(symbols):

    print(
        "\nUpdating trade_config.txt..."
    )


    # Create config folder if missing
    config_dir = os.path.dirname(
        TRADE_CONFIG_FILE
    )

    if not os.path.exists(config_dir):

        os.makedirs(
            config_dir,
            exist_ok=True
        )


    # Create empty config file if missing
    if not os.path.exists(
        TRADE_CONFIG_FILE
    ):

        print(
            "⚠ trade_config.txt not found. Creating new file..."
        )

        with open(
            TRADE_CONFIG_FILE,
            "w"
        ) as file:

            file.write(
                "# Auto generated trading configuration\n\n"
            )



    with open(
        TRADE_CONFIG_FILE,
        "r"
    ) as file:

        lines = file.readlines()



    new_lines = []

    inside = False

    section_found = False



    for line in lines:

        stripped = line.strip()


        # Start BLUECHIP section
        if stripped == "--BLUECHIP_STOCKS--":

            section_found = True

            inside = True


            new_lines.append(
                "--BLUECHIP_STOCKS--\n"
            )


            for symbol in symbols:

                new_lines.append(
                    f"{symbol}\n"
                )


            continue



        # Remove old BLUECHIP entries
        if inside:

            if stripped.startswith("--"):

                inside = False

                new_lines.append(
                    line
                )

            continue



        new_lines.append(
            line
        )



    # Add section if not present
    if not section_found:

        new_lines.append(
            "\n--BLUECHIP_STOCKS--\n"
        )


        for symbol in symbols:

            new_lines.append(
                f"{symbol}\n"
            )



    with open(
        TRADE_CONFIG_FILE,
        "w"
    ) as file:

        file.writelines(
            new_lines
        )


    print(
        "✅ trade_config.txt updated successfully"
    )

    print(
        f"Location: {TRADE_CONFIG_FILE}"
    )

# ======================================================
# MAIN
# ======================================================

def main():

    stocks = fetch_nifty50()


    ranked = []


    for symbol in stocks:

        try:

            data = analyse_stock(
                symbol
            )

            ranked.append(
                data
            )


        except Exception as e:

            print(
                f"Skipping {symbol}: {e}"
            )



    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    selected = [
        x["symbol"]
        for x in ranked[:TOP_STOCKS]
    ]



    print(
        "\n=============================="
    )

    print(
        "TOP BLUECHIP STOCKS"
    )

    print(
        "=============================="
    )


    for stock in selected:

        print(
            stock
        )


    update_trade_config(
        selected
    )



if __name__ == "__main__":

    main()
