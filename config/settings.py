import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access secrets securely
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

# Optional: print to verify (remove in production)
if __name__ == "__main__":
    print("API_KEY:", API_KEY)
    print("SECRET_KEY:", SECRET_KEY)
