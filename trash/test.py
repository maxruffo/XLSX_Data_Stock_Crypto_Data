import os
import pandas as pd

folder_path = "data/~index_ticker_list"

ticker_set = set()

# Durchsuche alle Unterordner
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith(".xlsx"):
            file_path = os.path.join(root, file)
            df = pd.read_excel(file_path)
            ticker_column = df["Ticker"].tolist()
            ticker_set.update(ticker_column)

ticker_list = list(ticker_set)

print(len(ticker_list))