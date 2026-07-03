# strategy/bluechip_strategy.py

import os
from account.ltp_fetcher import get_ltp
from account.quantity_calculator import calculate_quantity
from account.balance_checker import get_balance
from account.atp_fetcher import get_atp   # fetch ATP

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
    """Scan blue-chip stocks and return best candidate details as a dictionary."""
    trade_config = load_config()
    expected_profit_str = trade_config.get("EXPECTED_PROFIT", "").strip()

    if not expected_profit_str:
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
        return None

    print("✅ Running Bluechip Strategy")
    print(f"Available Margin: ₹{available_margin:.2f}")
    print(f"Target Profit: ₹{expected_profit:.2f}\n")

    best_candidate = None
    crossed_atp_candidates = []

    for symbol in bluechip_stocks:
        ltp = get_ltp(symbol)
        if not ltp:
            print(f"❌ Could not fetch LTP for {symbol}")
            continue

        qty, ltp = calculate_quantity(symbol, available_margin)
        estimated_profit = qty * 1.0  # assume ₹1 move
        target_price = ltp + (expected_profit / qty) if qty > 0 else None

        atp = get_atp(symbol)
        crossed_atp = None
        if atp:
            crossed_atp = ltp > atp
            status = "Crossed ATP (Bullish)" if crossed_atp else "Below ATP (Bearish)"
            atp_display = f"{atp:.2f}"
        else:
            status = "ATP not available"
            atp_display = "N/A"

        print(f"Symbol: {symbol}")
        print(f"  LTP: ₹{ltp:.2f}")
        print(f"  Quantity (after buffer): {qty}")
        if target_price:
            print(
                f"  Target Price for ₹{expected_profit} profit: ₹{target_price:.2f}")
        print(f"  ATP: {atp_display} → {status}")
        print()

        if crossed_atp:
            crossed_atp_candidates.append({
                "symbol": symbol,
                "ltp": round(ltp, 2),
                "quantity": qty,
                "target_price": round(target_price, 2) if target_price else None,
                "atp": atp_display,
                "estimated_profit": estimated_profit
            })
        elif not best_candidate or estimated_profit > best_candidate["estimated_profit"]:
            best_candidate = {
                "symbol": symbol,
                "ltp": round(ltp, 2),
                "quantity": qty,
                "target_price": round(target_price, 2) if target_price else None,
                "atp": atp_display,
                "estimated_profit": estimated_profit
            }

    # Final candidate decision
    if crossed_atp_candidates:
        best_candidate = max(crossed_atp_candidates,
                             key=lambda x: x["estimated_profit"])
        print(f"\n🎯 Best Candidate (Crossed ATP): {best_candidate['symbol']}")
    elif best_candidate:
        print(f"\n🎯 Best Candidate: {best_candidate['symbol']}")
    else:
        print("⚠️ No stock meets the profit target today.")
        return None

    # Return dictionary of details
    return best_candidate


if __name__ == "__main__":
    candidate = run_bluechip_strategy()
    if candidate:
        print("\n➡️ Final Selected Candidate Details:")
        print(candidate)
