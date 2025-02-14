from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class Config:
    AIPROXY_TOKEN = os.environ.get("AIPROXY_TOKEN")
    # Add more configuration variables as needed


config = Config()
