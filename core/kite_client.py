import os
from kiteconnect import KiteConnect
from config.settings import API_KEY, SECRET_KEY
from core.profile_viewer import show_profile

# Initialize Kite client once
kite = KiteConnect(api_key=API_KEY)


def generate_session(request_token: str):
    """
    Generate a new session using request_token and secret key.
    Returns the access_token for authenticated API calls.
    """
    data = kite.generate_session(request_token, api_secret=SECRET_KEY)
    access_token = data["access_token"]
    kite.set_access_token(access_token)
    return access_token


def get_profile():
    """
    Fetch user profile details after authentication.
    """
    return kite.profile()


def save_access_token_to_env(access_token: str, env_file=".env"):
    """
    Save the access_token into the existing .env file as ACCESS_TOKEN=XXXXXX.
    If ACCESS_TOKEN already exists, it will be updated.
    """
    lines = []
    found = False

    # Read existing .env
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            lines = f.readlines()

    # Update or add ACCESS_TOKEN
    for i, line in enumerate(lines):
        if line.startswith("ACCESS_TOKEN="):
            lines[i] = f"ACCESS_TOKEN={access_token}\n"
            found = True
            break

    if not found:
        lines.append(f"ACCESS_TOKEN={access_token}\n")

    # Write back to .env
    with open(env_file, "w") as f:
        f.writelines(lines)

    print(
        f"\n💾 Access token saved to {env_file} as ACCESS_TOKEN={access_token}")


def set_access_token(env_file=".env"):
    """
    Load ACCESS_TOKEN from .env and set it in Kite client.
    """
    access_token = None
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            for line in f:
                if line.startswith("ACCESS_TOKEN="):
                    access_token = line.strip().split("=")[1]
                    break

    if not access_token:
        raise Exception(
            "ACCESS_TOKEN not found in .env. Please authenticate first.")

    kite.set_access_token(access_token)
    return access_token


if __name__ == "__main__":
    # Step 1: Print login URL
    print("👉 Please log in using this URL:")
    print(kite.login_url())

    # Step 2: Wait for user to paste request_token
    request_token = input("\nPaste the request_token here: ").strip()

    try:
        # Step 3: Generate access token
        access_token = generate_session(request_token)
        print("\n✅ Authentication successful!")
        print("Access Token:", access_token)

        # Step 4: Save to .env
        save_access_token_to_env(access_token)

        # Step 5: Fetch and show profile
        profile = get_profile()
        show_profile(profile)

    except Exception as e:
        print("\n❌ Authentication failed:", str(e))
