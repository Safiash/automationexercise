import os
from dotenv import load_dotenv

load_dotenv()

USERNAME=os.getenv('USER')
PASSWORD=os.getenv('PASSWORD')
EMAIL=os.getenv('EMAIL')

BASE_URL="https://automationexercise.com/"
DEFAULT_BROWSER="chrome"
