from kiteconnect import KiteConnect
from config.settings import API_KEY, SECRET_KEY

# Initialize Kite client
kite = KiteConnect(api_key=API_KEY)


def generate_session(request_token: str):
    """
    Generate a session using request_token and secret key.
    Returns the access_token for authenticated API calls.
    """
    data = kite.generate_session(request_token, api_secret=SECRET_KEY)
    kite.set_access_token(data["access_token"])
    return data["access_token"]


def get_profile():
    """
    Fetch user profile details after authentication.
    """
    return kite.profile()


if __name__ == "__main__":
    print("Kite client initialized. Ready to authenticate.")
