import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_intraday_prices(tickers, period="1d", interval="1m"):
    data = yf.download(tickers=tickers, period=period, interval=interval, progress=False, group_by='ticker', threads=True)
    # Normalize to a tidy dataframe with columns: time, ticker, close
    frames = []
    if isinstance(tickers, str):
        tickers = [tickers]
    for t in tickers:
        try:
            df = data[t]['Close'].reset_index().rename(columns={'Datetime':'time','Close':'close'})
        except Exception:
            # Single ticker returns without top-level
            if 'Close' in data.columns:
                df = data['Close'].reset_index().rename(columns={'Datetime':'time','Close':'close'})
            else:
                continue
        df['ticker'] = t
        frames.append(df)
    if not frames:
        return pd.DataFrame(columns=['time','ticker','close'])
    out = pd.concat(frames, ignore_index=True)
    out = out.dropna().sort_values(['ticker','time'])
    return out
