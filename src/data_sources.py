import requests, feedparser, time
from typing import List, Dict
from .utils import clean_text, minutes_ago
from .config import TWITTER_BEARER_TOKEN, NEWSAPI_KEY, SEARCH_WINDOW_MIN, MAX_ITEMS

def search_twitter_recent(query: str, max_items: int = 50) -> List[Dict]:
    """Search recent tweets with Twitter/X API v2 Recent Search (if token present)."""
    if not TWITTER_BEARER_TOKEN:
        return []
    url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    params = {
        "query": query + " -is:retweet lang:en",
        "max_results": 100 if max_items > 100 else max_items,
        "tweet.fields": "created_at,lang,public_metrics",
        "start_time": minutes_ago(SEARCH_WINDOW_MIN),
    }
    r = requests.get(url, headers=headers, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    tweets = []
    for t in data.get("data", []):
        txt = clean_text(t.get("text",""))
        if not txt:
            continue
        tweets.append({
            "source": "twitter",
            "text": txt,
            "created_at": t.get("created_at"),
            "metrics": t.get("public_metrics", {}),
            "url": f"https://twitter.com/i/web/status/{t.get('id')}"
        })
        if len(tweets) >= max_items:
            break
    return tweets

def fetch_news_rss(query: str, max_items: int = 50) -> List[Dict]:
    """Simple RSS via Google News RSS for a query."""
    feed_url = f"https://news.google.com/rss/search?q={requests.utils.quote(query)}&hl=en-IN&gl=IN&ceid=IN:en"
    parsed = feedparser.parse(feed_url)
    items = []
    for e in parsed.entries[:max_items]:
        items.append({
            "source": "rss",
            "text": clean_text(e.get("title", "") + " " + (e.get("summary","") or "")),
            "created_at": e.get("published", ""),
            "url": e.get("link","")
        })
    return items

def fetch_newsapi(query: str, max_items: int = 50) -> List[Dict]:
    if not NEWSAPI_KEY:
        return []
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "from": minutes_ago(SEARCH_WINDOW_MIN),
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": max_items,
        "apiKey": NEWSAPI_KEY
    }
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    items = []
    for a in data.get("articles", []):
        items.append({
            "source": "newsapi",
            "text": clean_text((a.get("title","") or "") + " " + (a.get("description","") or "")),
            "created_at": a.get("publishedAt",""),
            "url": a.get("url","")
        })
    return items

def gather_texts_for_ticker(ticker: str, use_twitter=True, use_news=True, max_items=100):
    query = f"{ticker} OR {ticker} stock OR ({ticker} AND (earnings OR guidance OR upgrade OR downgrade OR results))"
    results = []
    if use_twitter:
        try:
            results += search_twitter_recent(query, max_items=max_items//2)
        except Exception as e:
            # fail-soft
            pass
    if use_news:
        try:
            results += fetch_news_rss(query, max_items=max_items//2)
        except Exception:
            pass
        try:
            results += fetch_newsapi(query, max_items=max_items//2)
        except Exception:
            pass
    return results[:max_items]
