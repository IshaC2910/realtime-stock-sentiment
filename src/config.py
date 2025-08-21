import os
from dotenv import load_dotenv

load_dotenv()

TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "").strip()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "").strip()

DEFAULT_TICKERS = ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "INFY", "RELIANCE.NS"]
SEARCH_WINDOW_MIN = 60  # how far back to search news/tweets (minutes)
MAX_ITEMS = 100  # max news/tweets to fetch per source
MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"
