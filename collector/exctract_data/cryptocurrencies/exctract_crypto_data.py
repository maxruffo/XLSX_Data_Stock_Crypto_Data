import os
import pandas as pd
import yfinance as yf
from datetime import datetime

data_folder = "data/cryptocurrencies"
target_folder = "data/cryptocurrencies"


def extract_tickers():
    tickers_list = []
    for root, dirs, files in os.walk(data_folder):
        for file in files:
            if file.endswith(".xlsx"):
                file_path = os.path.join(root, file)
                df = pd.read_excel(file_path)
                tickers = df['Ticker'].values.tolist()
                updated_tickers = [ticker + "-USD" for ticker in tickers]  # Hinzufügen von "-USD"
                tickers_list.extend(updated_tickers)

    return tickers_list


def save_ticker_to_error_file(crypto):
    error_folder = "errors/runtime"
    if not os.path.exists(error_folder):
        os.makedirs(error_folder)
    error_file = os.path.join(error_folder, "not_found_crypto.xlsx")
    not_found_df = pd.DataFrame({'Ticker': [crypto]})
    if os.path.exists(error_file):
        existing_data = pd.read_excel(error_file)
        updated_data = pd.concat([existing_data, not_found_df])
        updated_data.to_excel(error_file, index=False)
    else:
        not_found_df.to_excel(error_file, index=False)
    print(f"Das DataFrame für {crypto} ist leer. Tickersymbol wurde in '{error_file}' hinzugefügt.")
    print("\n")


def create_crypto_folder(crypto):
    crypto_folder = os.path.join(target_folder, crypto)
    if not os.path.exists(crypto_folder):
        os.makedirs(crypto_folder)
    return crypto_folder


def save_data_to_file(data, filename):
    if os.path.exists(filename):
        existing_data = pd.read_csv(filename, index_col='Date', parse_dates=True)
        data = pd.concat([existing_data, data]).drop_duplicates(subset='Date').reset_index(drop=True)

        data.to_csv(index=True, index_label='Date')
        print(f"Aktualisierte Daten wurden in {filename} gespeichert.")
    else:
        data.to_csv(filename, index=True, index_label='Date')
        print(f"Daten wurden in {filename} gespeichert.")
    print("\n")


def create_crypto_history_folder(crypto_folder):
    crypto_history_folder = os.path.join(crypto_folder, "history")
    if not os.path.exists(crypto_history_folder):
        os.makedirs(crypto_history_folder)
    return crypto_history_folder


def save_data_to_history_folder(data, crypto_history_folder):
    current_date = datetime.today().strftime('%Y-%m-%d')
    crypto_history_filename = os.path.join(crypto_history_folder, f"{current_date}.csv")

    if os.path.exists(crypto_history_filename):
        existing_data = pd.read_csv(crypto_history_filename, index_col='Date', parse_dates=True)
        data = pd.concat([existing_data, data]).drop_duplicates(subset='Date').reset_index(drop=True)


        data.to_csv(crypto_history_filename,index=True, index_label='Date')
        
        print(f"Aktualisierte Daten wurden in {crypto_history_filename} (historischer Ordner) gespeichert.")
    else:
        data.to_csv(crypto_history_filename, index=True, index_label='Date')
        print(f"Daten wurden in {crypto_history_filename} (historischer Ordner) gespeichert.")
    print("\n")
  


def download_crypto_data(crypto):
    try:
        data = yf.download(crypto, period='1d', interval='1m', progress=False)
        if data.empty:
            save_ticker_to_error_file(crypto)
            return

        # Erstellen der Spalte "Date" und Festlegen des Timestamps
        data['Date'] = data.index

        crypto_folder = create_crypto_folder(crypto)
        current_filename = os.path.join(crypto_folder, f"{crypto}.csv")
        save_data_to_file(data, current_filename)

        crypto_history_folder = create_crypto_history_folder(crypto_folder)
        save_data_to_history_folder(data, crypto_history_folder)
    except Exception as e:
        print(f"Fehler beim Herunterladen der Daten für {crypto}: {str(e)}")


def _run_crypto_extractor():
    ticker_set = extract_tickers()
    for crypto in ticker_set:
        download_crypto_data(crypto)
