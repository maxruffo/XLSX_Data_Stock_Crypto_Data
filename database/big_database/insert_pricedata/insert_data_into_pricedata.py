import os
import csv
import sqlite3
from datetime import datetime
import openpyxl

def check_and_insert_price_data(csv_file, ticker):
    try:
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
                    # Fehlerhafte Timestamps protokollieren
                    ws.append([ticker, row[0]])
                    print(f"Fehlerhafter Timestamp in der Datei {csv_file}: {row[0]}")
                    continue

                # Überprüfen, ob bereits ein Datensatz für den Ticker und Timestamp existiert
                cursor.execute("SELECT COUNT(*) FROM PriceData WHERE ticker=? AND timestamp=?", (ticker, timestamp))
                count = cursor.fetchone()[0]

                if count > 0:
                    print(f"Datensatz für {ticker} und {timestamp} befindet sich schon in der Datenbank")
                    # Datensatz bereits vorhanden, überspringen
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
    except Exception as e:
        # Fehler protokollieren
        ws.append([ticker, ""])
        print(f"Fehler beim Verarbeiten der Datei {csv_file}: {str(e)}")


def process_csv_folder(csv_folder, cursor, wb, ws):
    # Durchlaufen der Unterordner im CSV-Ordner
    for root, dirs, files in os.walk(csv_folder):
        for folder in dirs:
            ticker = folder

            # Überprüfen, ob der Ticker in der Datenbank existiert
            cursor.execute("SELECT COUNT(*) FROM Assets WHERE ticker=?", (ticker,))
            count = cursor.fetchone()[0]

            if count > 0:
                # Durchlaufen der CSV-Dateien im Unterordner "history"
                history_folder = os.path.join(root, folder, "history")
                for file in os.listdir(history_folder):
                    if file.endswith(".csv"):
                        csv_file = os.path.join(history_folder, file)
                        check_and_insert_price_data(csv_file, ticker)
                        print(f"Inserted PriceData for {ticker}")
            

def create_or_load_error_log(error_log_file):
    # Erstellen oder Öffnen der Fehlerprotokolldatei
    if not os.path.exists(error_log_file):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["Ticker", "Timestamp"])
    else:
        wb = openpyxl.load_workbook(error_log_file)
        ws = wb.active
    
    return wb, ws


# Pfad zur Fehlerprotokolldatei
error_log_file = "errors/runtime/database_error.xlsx"

# Verbindung zur Datenbank herstellen
conn = sqlite3.connect("database/database_db_files/database.db")
cursor = conn.cursor()

# Erstellen oder Öffnen der Fehlerprotokolldatei
wb, ws = create_or_load_error_log(error_log_file)



def _insert_pricedata():

    '''
    FÜR CRYPTO
    '''
    # Pfad zu den CSV-Dateien
    csv_folder = "data/cryptocurrencies"

    # Verarbeitung der CSV-Dateien
    process_csv_folder(csv_folder, cursor, wb, ws)

    # Änderungen in der Datenbank speichern
    conn.commit()

    # Fehlerprotokolldatei speichern
    wb.save(error_log_file)


    '''
    FÜR AKTIEN
    '''
    # Pfad zu den CSV-Dateien
    csv_folder = "data/stocks"


    # Verarbeitung der CSV-Dateien
    process_csv_folder(csv_folder, cursor, wb, ws)

    # Änderungen in der Datenbank speichern
    conn.commit()

    # Fehlerprotokolldatei speichern
    wb.save(error_log_file)

    # Verbindung zur Datenbank schließen
    conn.close()


_insert_pricedata()