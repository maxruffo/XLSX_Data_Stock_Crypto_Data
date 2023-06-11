import sqlite3
import os
import csv
from datetime import datetime

def insert_price_data(database_path, ticker):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    folders = ['stocks', 'cryptocurrencies']
    for folder in folders:
        folder_path = f"data/{folder}/{ticker}/history"
        if os.path.exists(folder_path):
            # Durchlaufe den Ordner "history" des Tickers
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.endswith('.csv'):
                        csv_file = os.path.join(root, file)

                        # CSV-Datei öffnen und Daten einfügen
                        with open(csv_file, "r") as file:
                            reader = csv.reader(file)
                            next(reader)  # Header überspringen

                            for row in reader:
                                try:
                                    timestamp_str = row[0].split("+")[0]  # Timestamp-Bestandteil extrahieren
                                    timestamp_str = timestamp_str[:19]
                                    timestamp_offset = timestamp_str[19:]
                                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                                except ValueError:
                                    print(f"Fehlerhafter Timestamp in der Datei {csv_file}: {row[0]}")
                                    continue

                                open_price = float(row[1])
                                high_price = float(row[2])
                                low_price = float(row[3])
                                close_price = float(row[4])
                                adj_close_price = float(row[5])
                                volume = float(row[6])

                                # Datensatz in die Tabelle "PriceData" einfügen
                                cursor.execute("INSERT INTO PriceData (ticker, timestamp, timestamp_offset, open, high, low, close, adj_close, volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                               (ticker, timestamp, timestamp_offset, open_price, high_price, low_price, close_price, adj_close_price, volume))

            break

    # Änderungen speichern und die Verbindung zur Datenbank schließen
    conn.commit()
    conn.close()

    print(f"Preisdaten für {ticker} wurden in die Datenbank eingefügt.")


if __name__ == "__main__":
    ticker = input("Geben Sie den Ticker ein: ")  # Beispiel: BTC (für Kryptowährungen) oder AAPL (für Aktien)
    database_file = f"{ticker}.db"
    database_path = os.path.join("database", database_file)

    # Überprüfen, ob die Datenbankdatei bereits existiert
    if not os.path.exists(database_path):
        # Datenbankdatei erstellen
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # Tabellen erstellen
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS PriceData (
                ticker TEXT NOT NULL,
                timestamp DATE NOT NULL,
                timestamp_offset TEXT NOT NULL,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                adj_close REAL,
                volume REAL,
                PRIMARY KEY (ticker, timestamp)
            )
        ''')

        #Änderungen speichern und die Verbindung zur Datenbank schließen
        conn.commit()
        conn.close()
        print(f'Datenbankdatei {database_file} wurde erstellt.')

    # Preisdaten in die Datenbank einfügen
    insert_price_data(database_path, ticker)
