import os
from dotenv import load_dotenv


# =====================================================
# PROJECT ROOT
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================

ENV_FILE = os.path.join(
    BASE_DIR,
    ".env"
)

load_dotenv(
    ENV_FILE
)


# =====================================================
# SECRETS
# =====================================================

API_KEY = os.getenv(
    "API_KEY"
)

SECRET_KEY = os.getenv(
    "SECRET_KEY"
)

ACCESS_TOKEN = os.getenv(
    "ACCESS_TOKEN"
)


# =====================================================
# FILE PATHS
# =====================================================

TRADE_CONFIG_FILE = os.path.join(
    BASE_DIR,
    "config",
    "trade_config.txt"
)


LOG_FILE = os.path.join(
    BASE_DIR,
    "Reports",
    "trade_log.xlsx"
)


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    print(
        "BASE_DIR:",
        BASE_DIR
    )

    print(
        "API_KEY:",
        API_KEY
    )

    print(
        "SECRET_KEY:",
        SECRET_KEY
    )

    print(
        "ACCESS_TOKEN:",
        ACCESS_TOKEN
    )

    print(
        "TRADE_CONFIG_FILE:",
        TRADE_CONFIG_FILE
    )

    print(
        "LOG_FILE:",
        LOG_FILE
    )
