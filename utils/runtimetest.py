import yfinance as yf
import datetime as datetime2

today = datetime2.date.today()
yesterday = today - datetime2.timedelta(days=1)


data = yf.download("BTC-USD", period='1d', interval='1m',start=yesterday,end=today, progress=False)

print(data)