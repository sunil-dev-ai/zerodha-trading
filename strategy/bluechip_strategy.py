# strategy/bluechip_strategy.py

import os
from account.ltp_fetcher import get_ltp
from account.quantity_calculator import calculate_quantity
from account.balance_checker import get_balance

CONFIG_FILE = os.path.join("config", "trade_config.txt")


def load_config(config_file=CONFIG_FILE):
    """Load key-value pairs from trade_config.txt into a dictionary."""
    config = {}
    try:
        with open(config_file, "r") as f:
            for line in f:
                line = line.strip()
                if not line or "=" not in line or line.startswith("#"):
                    continue
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
    except FileNotFoundError:
        print("❌ trade_config.txt not found in config folder.")
    return config


def load_section(section_name: str, config_file=CONFIG_FILE):
    """Load a section (like --BLUECHIP_STOCKS--) from trade_config.txt."""
    stocks = []
    try:
        with open(config_file, "r") as f:
            lines = f.readlines()
            capture = False
            for line in lines:
                line = line.strip()
                if line == section_name:
                    capture = True
                    continue
                if capture:
                    if line.startswith("--") or not line:
                        break
                    if "," in line:
                        stocks.extend([s.strip().upper()
                                      for s in line.split(",")])
                    else:
                        stocks.append(line.upper())
    except FileNotFoundError:
        print("❌ trade_config.txt not found in config folder.")
    return stocks


def run_bluechip_strategy():
    """
    Scan blue-chip stocks from config file and calculate potential trades
    aiming for at least EXPECTED_PROFIT rupees.
    """
    trade_config = load_config()
    expected_profit_str = trade_config.get("EXPECTED_PROFIT", "").strip()

    if not expected_profit_str:
        # Prompt user if EXPECTED_PROFIT is missing or empty
        expected_profit_str = input("Enter expected profit amount: ").strip()

    try:
        expected_profit = float(expected_profit_str)
    except ValueError:
        print("❌ Invalid profit value entered. Defaulting to 100.")
        expected_profit = 100.0

    balance = get_balance()
    available_margin = balance["net"]

    bluechip_stocks = load_section("--BLUECHIP_STOCKS--")
    if not bluechip_stocks:
        print("❌ No BLUECHIP_STOCKS defined in trade_config.txt")
        return

    print("✅ Running Bluechip Strategy")
    print(f"Available Margin: ₹{available_margin:.2f}")
    print(f"Target Profit: ₹{expected_profit:.2f}\n")

    best_candidate = None
    best_profit = 0

    for symbol in bluechip_stocks:
        ltp = get_ltp(symbol)
        if not ltp:
            print(f"❌ Could not fetch LTP for {symbol}")
            continue

        qty, ltp = calculate_quantity(symbol, available_margin)
        estimated_profit = qty * 1.0  # assume ₹1 move

        print(f"Symbol: {symbol}")
        print(f"  LTP: ₹{ltp:.2f}")
        print(f"  Quantity (after buffer): {qty}")
        print(f"  Estimated Profit (₹1 move): ₹{estimated_profit:.2f}")

        if estimated_profit >= expected_profit:
            print(f"  ✅ Meets profit target of ₹{expected_profit}\n")
        else:
            print(f"  ⚠️ Below profit target\n")

        if estimated_profit > best_profit:
            best_profit = estimated_profit
            best_candidate = symbol

    if best_candidate:
        print(
            f"🎯 Best Candidate: {best_candidate} (Estimated Profit: ₹{best_profit:.2f})")
    else:
        print("⚠️ No stock meets the profit target today.")


if __name__ == "__main__":
    run_bluechip_strategy()
