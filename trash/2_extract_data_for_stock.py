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

        current_number = 0
        # Schleife über die Aktiensymbole
        for stock in stocks:
            try:
                current_number =+ 1
                print(f"Stock Number: {current_number}")
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
                stock_folder = f"{data_folder}/{stock}"
                if not os.path.exists(stock_folder):
                    os.makedirs(stock_folder)

                # Dateiname für den aktuellen Tag erstellen
                current_date = datetime.today().strftime('%Y-%m-%d')
                current_filename = f"{stock_folder}/{stock}.csv"

                if os.path.exists(current_filename):
                    # Daten für den aktuellen Tag bereits vorhanden, aktualisieren
                    data = pd.read_csv(current_filename, index_col=0)
                    latest_data = yf.download(stock, period='1d', interval='1m', progress=False)
                    updated_data = pd.concat([data, latest_data])
                    updated_data.to_csv(current_filename)
                    print(f"Aktualisierte Daten für {stock} wurden in {current_filename} gespeichert.")
                else:
                    # Daten für den aktuellen Tag herunterladen und speichern
                    data = yf.download(stock, period='1d', interval='1m', progress=False)
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
                print("\n")
            except Exception as e:
                print(f"Fehler beim Herunterladen der Daten für {stock}: {str(e)}")



