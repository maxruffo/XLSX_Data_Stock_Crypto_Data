import os
import pandas as pd

data_folder = "data/~index_ticker_list"


def exctract_tickers():
    tickers_set = set()
    for root, dirs, files in os.walk(data_folder):
        for file in files:
            if file.endswith(".xlsx"):
                file_path = os.path.join(root, file)
                df = pd.read_excel(file_path)
                tickers = set(df['Ticker'].values)
                tickers_set.update(tickers)


    
    return sorted(tickers_set)


print(exctract_tickers())


