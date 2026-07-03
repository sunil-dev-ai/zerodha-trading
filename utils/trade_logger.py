# util/trade_logger.py

import os
import pandas as pd
from datetime import datetime
from config.settings import LOG_FILE


def log_trade(symbol: str, qty: int, buy_price: float, sell_price: float, profit: float):
    """Log trade details into an Excel file."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entry = {
        "DateTime": now,
        "Symbol": symbol,
        "Quantity": qty,
        "BuyPrice": round(buy_price, 2),
        "SellPrice": round(sell_price, 2),
        "Profit": round(profit, 2)
    }

    # If file exists, append; else create new
    if os.path.exists(LOG_FILE):
        df = pd.read_excel(LOG_FILE)
        df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    else:
        df = pd.DataFrame([entry])

    df.to_excel(LOG_FILE, index=False)
    print(f"📝 Trade logged in {LOG_FILE}")
