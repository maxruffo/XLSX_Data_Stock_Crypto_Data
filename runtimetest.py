import yfinance as yf
import datetime as datetime2

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)


data = yf.download("AMC", period='1d', interval='1m',start=yesterday,end=today, progress=False)

print(data)