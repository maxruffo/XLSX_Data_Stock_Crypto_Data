import os
import pandas as pd


def concat_file_for_ticker(ticker):
    data_folders = ["data/stocks", "data/cryptocurrencies"]
    merged_df = pd.DataFrame()

    for folder in data_folders:
        ticker_folder = os.path.join(folder, ticker)
        history_folder = os.path.join(ticker_folder, "history")

        if os.path.exists(history_folder):
            for root, dirs, files in os.walk(history_folder):
                for file in files:
                    print(file)
                    if file.endswith(".csv"):
                        file_path = os.path.join(root, file)
                        df = pd.read_csv(file_path, index_col='Date', parse_dates=True)
                        merged_df = pd.concat([merged_df, df])

    return merged_df