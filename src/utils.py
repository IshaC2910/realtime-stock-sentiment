import re, datetime as dt
from typing import List, Dict

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"http\S+", "", text)         # URLs
    text = re.sub(r"\s+", " ", text).strip()
    return text

def now_utc():
    return dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc)

def minutes_ago(n: int) -> str:
    return (now_utc() - dt.timedelta(minutes=n)).isoformat()
