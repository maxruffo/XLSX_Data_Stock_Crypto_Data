import yfinance as yf
import datetime as datetime

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

data = yf.download("AAPL", period='1d', interval='1m',start=yesterday,end=today, progress=False)

