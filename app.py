import streamlit as st
import pandas as pd
from src.config import DEFAULT_TICKERS, MODEL_NAME
from src.data_sources import gather_texts_for_ticker
from src.sentiment import SentimentEngine
from src.prices import get_intraday_prices

st.set_page_config(page_title="Real-Time Stock Sentiment", layout="wide")

st.title("📈 Real-Time Stock Market Sentiment Analyzer")
st.caption("No IoT. Streams news & Twitter (optional) + yfinance prices. Not financial advice.")

with st.sidebar:
    st.header("⚙️ Settings")
    tickers = st.multiselect("Select tickers", DEFAULT_TICKERS, default=["AAPL","TSLA","INFY"])
    use_twitter = st.toggle("Use Twitter/X", value=False, help="Enable if you have a Bearer Token in .env")
    use_news = st.toggle("Use News", value=True)
    max_items = st.slider("Max texts per ticker", 20, 200, 80, step=20)
    st.divider()
    st.caption("Model: " + MODEL_NAME)

@st.cache_resource(show_spinner=True)
def load_engine():
    return SentimentEngine(MODEL_NAME)

engine = load_engine()

tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📰 Stream", "⚠️ Notes"])

with tab1:
    st.subheader("Market Mood by Ticker")
    summary_rows = []
    stream_rows = []
    with st.spinner("Fetching streams and prices..."):
        price_df = get_intraday_prices(tickers, period="1d", interval="1m")
        for t in tickers:
            texts = gather_texts_for_ticker(t, use_twitter=use_twitter, use_news=use_news, max_items=max_items)
            contents = [d["text"] for d in texts]
            preds = engine.predict(contents)
            for d, p in zip(texts, preds):
                stream_rows.append({
                    "ticker": t,
                    "source": d.get("source"),
                    "text": d.get("text"),
                    "url": d.get("url"),
                    **p
                })
            if preds:
                scores = [p["score"] for p in preds]
                avg = sum(scores)/len(scores)
                label = "Bullish" if avg > 0.1 else ("Bearish" if avg < -0.1 else "Neutral")
            else:
                avg, label = 0.0, "Neutral"
            summary_rows.append({"ticker": t, "sentiment": avg, "label": label, "n_texts": len(preds)})
    summary_df = pd.DataFrame(summary_rows).sort_values("sentiment", ascending=False)
    st.dataframe(summary_df, use_container_width=True)

    st.subheader("Intraday Price (1m)")
    if not price_df.empty:
        import plotly.express as px
        for t in tickers:
            sub = price_df[price_df["ticker"]==t]
            if sub.empty: 
                continue
            fig = px.line(sub, x="time", y="close", title=f"{t} price")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No intraday price data returned (possibly outside market hours or ticker not supported).")

with tab2:
    st.subheader("Latest Text Stream with Sentiment")
    if stream_rows:
        stream_df = pd.DataFrame(stream_rows).sort_values("pos", ascending=False)
        st.dataframe(stream_df[["ticker","source","score","pos","neg","neu","text","url"]], use_container_width=True, height=500)
        st.caption("Tip: Click column headers to sort.")
    else:
        st.warning("No texts retrieved. Add API keys or enable News RSS.")

with tab3:
    st.markdown("""
- **Twitter/X** requires a Bearer Token set in `.env` (`TWITTER_BEARER_TOKEN`).  
- **News** uses Google News RSS by default; **NewsAPI** is optional.  
- Sentiment model: `cardiffnlp/twitter-roberta-base-sentiment-latest`.  
- Prices via `yfinance`, intraday 1-minute candles (subject to Yahoo limitations).
- This tool is **educational** and **not financial advice**.
    """)
