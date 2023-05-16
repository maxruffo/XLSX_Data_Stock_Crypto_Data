import os
import pandas as pd
import yfinance as yf
from datetime import datetime

data_folder = "data/stocks/~index_ticker_list"
target_folder = "data/stocks"

def extract_tickers():
    tickers_set = set()
    for root, dirs, files in os.walk(data_folder):
        for file in files:
            if file.endswith(".xlsx"):
                file_path = os.path.join(root, file)
                df = pd.read_excel(file_path)
                tickers = set(df['Ticker'].values)
                tickers_set.update(tickers)
    return sorted(tickers_set)


def save_ticker_to_error_file(stock):
    error_folder = "errors/runtime"
    if not os.path.exists(error_folder):
        os.makedirs(error_folder)
    error_file = os.path.join(error_folder, "not_found_stock.xlsx")
    not_found_df = pd.DataFrame({'Ticker': [stock]})
    if os.path.exists(error_file):
        existing_data = pd.read_excel(error_file)
        updated_data = pd.concat([existing_data, not_found_df])
        updated_data.to_excel(error_file, index=False)
    else:
        not_found_df.to_excel(error_file, index=False)
    print(f"Das DataFrame für {stock} ist leer. Tickersymbol wurde in '{error_file}' hinzugefügt.")
    print("\n")

def create_stock_folder(stock):
    stock_folder = os.path.join(target_folder, stock)
    if not os.path.exists(stock_folder):
        os.makedirs(stock_folder)
    return stock_folder


def save_data_to_file(data, filename):
    if os.path.exists(filename):
        existing_data = pd.read_csv(filename, index_col='Datetime', parse_dates=True)
        data = pd.concat([existing_data, data]).loc[~pd.concat([existing_data, data]).index.duplicated(keep='first')]
        data.to_csv(filename)
        print(f"Aktualisierte Daten wurden in {filename} gespeichert.")
    else:
        data.to_csv(filename, index=False)
        print(f"Daten wurden in {filename} gespeichert.")
    print("\n")


def create_stock_history_folder(stock_folder):
    stock_history_folder = os.path.join(stock_folder, "history")
    if not os.path.exists(stock_history_folder):
        os.makedirs(stock_history_folder)
    return stock_history_folder


def save_data_to_history_folder(data, stock_history_folder):
    current_date = datetime.today().strftime('%Y-%m-%d')
    stock_history_filename = os.path.join(stock_history_folder, f"{current_date}.csv")

    if os.path.exists(stock_history_filename):
        existing_data = pd.read_csv(stock_history_filename, index_col='Datetime', parse_dates=True)
        data = pd.concat([existing_data, data]).loc[~pd.concat([existing_data, data]).index.duplicated(keep='first')]
        data.to_csv(stock_history_filename)
        print(f"Aktualisierte Daten wurden in {stock_history_filename} (historischer Ordner) gespeichert.")
    else:
        data.to_csv(stock_history_filename, index=False)
        print(f"Daten wurden in {stock_history_filename} (historischer Ordner) gespeichert.")
    print("\n")



def download_stock_data(stock):
    try:
        data = yf.download(stock, period='1d', interval='1m', progress=False)
        if data.empty:
            save_ticker_to_error_file(stock)
            return

        stock_folder = create_stock_folder(stock)
        current_filename = os.path.join(stock_folder, f"{stock}.csv")
        save_data_to_file(data, current_filename)

        stock_history_folder = create_stock_history_folder(stock_folder)
        save_data_to_history_folder(data, stock_history_folder)
    except Exception as e:
        print(f"Fehler beim Herunterladen der Daten für {stock}: {str(e)}")


def _run_stock_extractor():
    ticker_set = extract_tickers()
    for stock in ticker_set:
        download_stock_data(stock)
