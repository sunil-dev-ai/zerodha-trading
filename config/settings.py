import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access secrets securely
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

# File path for unified trading config storage
TRADE_CONFIG_FILE = os.path.join("config", "trade_config.txt")

# File path for trade log storage
LOG_FILE = os.path.join("Reports", "trade_log.xlsx")

if __name__ == "__main__":
    print("API_KEY:", API_KEY)
    print("SECRET_KEY:", SECRET_KEY)
    print("ACCESS_TOKEN:", ACCESS_TOKEN)
    print("TRADE_CONFIG_FILE:", TRADE_CONFIG_FILE)
    print("LOG_FILE:", LOG_FILE)
