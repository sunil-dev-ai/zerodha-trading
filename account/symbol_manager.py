import os
from config.settings import TRADE_CONFIG_FILE


def load_trade_config():
    """Load trading config values from file."""
    config = {"SYMBOL": None, "EXPECTED_PROFIT": None, "MAX_LOSS": None}
    if os.path.exists(TRADE_CONFIG_FILE):
        with open(TRADE_CONFIG_FILE, "r") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    config[key] = value
    return config


def save_trade_config(symbol, expected_profit, max_loss):
    """Save trading config values to file."""
    with open(TRADE_CONFIG_FILE, "w") as f:
        f.write(f"SYMBOL={symbol.upper()}\n")
        f.write(f"EXPECTED_PROFIT={expected_profit}\n")
        f.write(f"MAX_LOSS={max_loss}\n")


def get_trade_config():
    """
    Get symbol, expected profit, and max loss.
    If missing, prompt user and save to file.
    """
    config = load_trade_config()

    if not config["SYMBOL"]:
        config["SYMBOL"] = input(
            "Enter trading symbol (e.g., INFY, RELIANCE): ").strip().upper()
    if not config["EXPECTED_PROFIT"]:
        config["EXPECTED_PROFIT"] = input(
            "Enter expected profit amount: ").strip()
    if not config["MAX_LOSS"]:
        config["MAX_LOSS"] = input("Enter max loss amount: ").strip()

    # Save back for reuse
    save_trade_config(config["SYMBOL"],
                      config["EXPECTED_PROFIT"], config["MAX_LOSS"])
    return config


if __name__ == "__main__":
    trade_config = get_trade_config()
    print("✅ Trading Config Loaded")
    print("SYMBOL:", trade_config["SYMBOL"])
    print("EXPECTED_PROFIT:", trade_config["EXPECTED_PROFIT"])
    print("MAX_LOSS:", trade_config["MAX_LOSS"])
