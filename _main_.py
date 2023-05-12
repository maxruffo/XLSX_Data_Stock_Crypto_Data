import os
import yfinance as yf
import pandas as pd
from datetime import datetime

# Liste der Aktiensymbole
stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'FB', 'TSLA']  # Fügen Sie hier weitere Aktiensymbole hinzu

# Erstellen des Ordners 'data', wenn er nicht existiert
data_folder = 'data'
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

        # Ordner für die historischen Daten erstellen
        history_folder = f"{stock_folder}/history"
        if not os.path.exists(history_folder):
            os.makedirs(history_folder)

        # Daten für den aktuellen Tag in den historischen Ordner kopieren
        history_filename = f"{history_folder}/{current_date}.csv"
        data.to_csv(history_filename)
        print(f"Daten für {stock} wurden in {history_filename} (historischer Ordner) gespeichert.")
        
    except Exception as e:
        print(f"Fehler beim Herunterladen der Daten für {stock}: {str(e)}")
