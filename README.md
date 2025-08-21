# Real-Time Stock Market Sentiment Analyzer (No IoT)

A Streamlit web app that pulls **live news and Twitter/X posts**, runs **NLP sentiment analysis**, and combines it with **real-time stock prices** to show an overall **bullish/bearish/neutral** market mood for selected tickers.

> Designed to be **easy to run** on **Google Colab**, deploy on **Hugging Face Spaces**, or host locally. Twitter/News sources are **optional** and auto-disable if no API keys are provided.

---

## ✨ Features
- Real-time(ish) stock price updates via `yfinance`
- Live text stream from:
  - **Twitter/X** (Recent Search, v2) — optional
  - **News** via RSS (no key) and **NewsAPI** (optional)
- Robust sentiment with a Hugging Face transformer (`cardiffnlp/twitter-roberta-base-sentiment-latest`)
- Clean Streamlit dashboard with:
  - Ticker selector
  - Sentiment gauges & aggregates
  - Top positive/negative recent posts
  - Price chart & sentiment trend

---

## 🧰 Tech Stack
- **Python**, **Streamlit**
- **transformers** (Hugging Face) for sentiment
- **yfinance** for prices
- **requests**, **feedparser** for data ingestion

---

## 🗂️ Project Structure

```
realtime-stock-sentiment/
├─ app.py
├─ requirements.txt
├─ .env.example
├─ README.md
└─ src/
   ├─ config.py
   ├─ data_sources.py
   ├─ sentiment.py
   ├─ prices.py
   └─ utils.py
```

---

## 🚀 Quickstart (Local)
```bash
pip install -r requirements.txt
cp .env.example .env  # fill in tokens if you have them
streamlit run app.py
```
Open the URL shown in your terminal.

---

## ▶️ Run on Google Colab (with public share link)
1. Open a new notebook and run the following cell:
```python
!git clone https://github.com/your-username/realtime-stock-sentiment.git
%cd realtime-stock-sentiment
!pip install -r requirements.txt
import os, shutil
# (Optional) add your secrets
from google.colab import userdata
open('.env','w').write(f"TWITTER_BEARER_TOKEN={userdata.get('TWITTER_BEARER_TOKEN','')}
NEWSAPI_KEY={userdata.get('NEWSAPI_KEY','')}
")
# Start Streamlit with public URL
from pyngrok import ngrok
public_url = ngrok.connect(8501).public_url
print('Public URL:', public_url)
!streamlit run app.py --server.port 8501 &
```
2. Open the printed **Public URL**.

> If `google.colab.userdata` is not available, just create the `.env` manually:
```python
open('.env','w').write("TWITTER_BEARER_TOKEN=
NEWSAPI_KEY=
")
```

---

## ☁️ Deploy on Hugging Face Spaces (Streamlit)
1. Create a new **Space** → **Streamlit**.
2. Upload these files: `app.py`, `requirements.txt`, `src/` folder, `.env.example`, `README.md`.
3. Set **Space variables** (Settings → Variables and secrets):
   - `TWITTER_BEARER_TOKEN`
   - `NEWSAPI_KEY`
4. The app will build and run automatically. Share the Space URL.

---

## 🔑 Optional API Keys
- **Twitter/X**: Create a project at https://developer.x.com/ and get a **Bearer Token** (Recent Search).
- **NewsAPI**: https://newsapi.org/

The app auto-falls-back to **RSS-only** if no keys are provided.

---

## ⚠️ Notes & Limits
- `yfinance` updates are near-real-time for `interval="1m"` and `period <= 7d"` (subject to Yahoo limits).
- Twitter/X API access depends on your account level.
- This tool is **not financial advice**.

---

## 📝 License
MIT
