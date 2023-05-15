import os
import pandas as pd
import yfinance as yf
from datetime import datetime

data_folder = "data/~index_ticker_list/"

# Durchlaufen der Ordner in "data/~index_ticker_list/"
for folder_name in os.listdir(data_folder):
    folder_path = os.path.join(data_folder, folder_name)

    # Überprüfen, ob es sich um einen Ordner handelt
    if os.path.isdir(folder_path):
        # Erstellen des Zielordners in data/
        target_folder = os.path.join("data", folder_name)
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        # Erstellen eines Sets für die eindeutigen Ticker-Einträge
        ticker_set = set()

        # Durchlaufen der XLSX-Dateien im aktuellen Ordner
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            # Überprüfen, ob es sich um eine XLSX-Datei handelt
            if file_name.endswith(".xlsx"):
                # Daten aus der XLSX-Datei lesen
                df = pd.read_excel(file_path)

                # Hinzufügen der Ticker-Einträge zum Set
                ticker_set.update(df["Ticker"].tolist())

        # Speichern der eindeutigen Ticker-Einträge als CSV-Datei im Zielordner
        data_folder = target_folder
        stocks = ticker_set
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

# Schleife über die Aktiensymbole
        for stock in stocks:
            try:
                # Ordner für die jeweilige Aktie erstellen
                stock_folder = f"{data_folder}/{stock}"
                if not os.path.exists(stock_folder):
                    os.makedirs(stock_folder)

                # Dateiname für den aktuellen Tag erstellen
                current_date = datetime.today().strftime('%Y-%m-%d')
                current_filename = f"{stock_folder}/{stock}.csv"

                if os.path.exists(current_filename):
                    # Daten für den aktuellen Tag bereits vorhanden, aktualisieren
                    data = pd.read_csv(current_filename, index_col=0)
                    latest_data = yf.download(stock, period='1d', interval='1m')
                    updated_data = pd.concat([data, latest_data])
                    updated_data.to_csv(current_filename)
                    print(f"Aktualisierte Daten für {stock} wurden in {current_filename} gespeichert.")
                else:
                    # Daten für den aktuellen Tag herunterladen und speichern
                    data = yf.download(stock, period='1d', interval='1m')
                    data.to_csv(current_filename)
                    print(f"Daten für {stock} wurden in {current_filename} gespeichert.")

                # Ordner für die historischen Daten der Aktie erstellen
                stock_history_folder = f"{stock_folder}/history"
                if not os.path.exists(stock_history_folder):
                    os.makedirs(stock_history_folder)

                # Daten für den aktuellen Tag in den historischen Ordner der Aktie kopieren
                stock_history_filename = f"{stock_history_folder}/{current_date}.csv"
                data.to_csv(stock_history_filename)
                print(f"Daten für {stock} wurden in {stock_history_filename} (historischer Ordner) gespeichert.")

            except Exception as e:
                print(f"Fehler beim Herunterladen der Daten für {stock}: {str(e)}")

            
        
        