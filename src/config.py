import os
import sys
sys.path.append(os.path.abspath('.'))

import json
from dotenv import load_dotenv

def get_config():
    with open("config.json") as f:
        res= json.load(f)
    return res
    
def get_credentials():
    load_dotenv()
    # Twitter API credentials
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TWITTER_API_CONSUMER_KEY = os.getenv("TWITTER_API_CONSUMER_KEY")

    TWITTER_API_CONSUMER_SECRET = os.getenv("TWITTER_API_CONSUMER_SECRET")
    TWITTER_API_BEARER_TOKEN = os.getenv("TWITTER_API_BEARER_TOKEN")
    TWITTER_API_ACCESS_TOKEN = os.getenv("TWITTER_API_ACCESS_TOKEN")
    TWITTER_API_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_API_ACCESS_TOKEN_SECRET")
    TWITTER_user_name=os.getenv("TWITTER_user_name")
    TWITTER_email=os.getenv("TWITTER_email")
    TWITTER_pwd=os.getenv("TWITTER_pwd")
    return {
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "TWITTER_API_CONSUMER_KEY": TWITTER_API_CONSUMER_KEY,
        "TWITTER_API_CONSUMER_SECRET": TWITTER_API_CONSUMER_SECRET,
        "TWITTER_API_BEARER_TOKEN": TWITTER_API_BEARER_TOKEN,
        "TWITTER_API_ACCESS_TOKEN": TWITTER_API_ACCESS_TOKEN,
        "TWITTER_API_ACCESS_TOKEN_SECRET": TWITTER_API_ACCESS_TOKEN_SECRET,
        "TWITTER_user_name":TWITTER_user_name,
        "TWITTER_email":TWITTER_email,
        "TWITTER_pwd":TWITTER_pwd
    }

def get_prompt():
    with open("data/prompt.json") as f:
        res = json.load(f)
    return res