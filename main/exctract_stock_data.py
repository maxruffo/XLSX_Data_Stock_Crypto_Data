import os
import pandas as pd
import yfinance as yf
from datetime import datetime

target_folder = "data/stocks"

# Durchlaufen der Ordner in "data/~index_ticker_list/"


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


ticker_set = exctract_tickers()

for stock in ticker_set:
    try:
        # Überprüfen, ob das DataFrame leer ist
        data = yf.download(stock, period='1d', interval='1m', progress=False)
        if data.empty:
            # Datenframe ist leer, speichern des Tickersymbols in einer separaten xlsx-Datei
            error_folder = "errors/runtime"
            if not os.path.exists(error_folder):
                os.makedirs(error_folder)
            error_file = os.path.join(error_folder, "not_found_stock.xlsx")
            not_found_df = pd.DataFrame({'Ticker': [stock]})
            if os.path.exists(error_file):
                # Falls die Datei bereits existiert, die neue Zeile hinzufügen
                existing_data = pd.read_excel(error_file)
                updated_data = pd.concat([existing_data, not_found_df])
                updated_data.to_excel(error_file, index=False)
            else:
                # Falls die Datei noch nicht existiert, eine neue Datei erstellen
                not_found_df.to_excel(error_file, index=False)
            print(f"Das DataFrame für {stock} ist leer. Tickersymbol wurde in '{error_file}' hinzugefügt.")
           
            continue
           

        # Ordner für die jeweilige Aktie erstellen
        stock_folder = os.path.join(target_folder, stock)
        if not os.path.exists(stock_folder):
            os.makedirs(stock_folder)

        # Dateiname für den aktuellen Tag erstellen
        current_date = datetime.today().strftime('%Y-%m-%d')
        current_filename = os.path.join(stock_folder, f"{stock}.csv")

        if os.path.exists(current_filename):
            # Daten für den aktuellen Tag bereits vorhanden, aktualisieren
            data.to_csv(current_filename, mode='a', header=False)
            print(f"Aktualisierte Daten für {stock} wurden in {current_filename} gespeichert.")
        else:
            # Daten für den aktuellen Tag herunterladen und speichern
            data.to_csv(current_filename)
            print(f"Daten für {stock} wurden in {current_filename} gespeichert.")

        # Ordner für die historischen Daten der Aktie erstellen
        stock_history_folder = os.path.join(stock_folder, "history")
        if not os.path.exists(stock_history_folder):
            os.makedirs(stock_history_folder)

        # Daten für den aktuellen Tag in den historischen Ordner der Aktie kopieren
        stock_history_filename = os.path.join(stock_history_folder, f"{current_date}.csv")
        data.to_csv(stock_history_filename)
        print(f"Daten für {stock} wurden in {stock_history_filename} (historischer Ordner) gespeichert.")
        print("\n")
    except Exception as e:
        print(f"Fehler beim Herunterladen der Daten für {stock}: {str(e)}")
