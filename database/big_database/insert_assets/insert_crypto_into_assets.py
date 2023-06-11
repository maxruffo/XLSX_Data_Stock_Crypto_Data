import sqlite3
import openpyxl



def _insert_crypto():

    # Pfad zur XLSX-Datei
    xlsx_file = "data/cryptocurrencies/~index_cryptocurrencies_list.xlsx"

    # Verbindung zur Datenbank herstellen
    conn = sqlite3.connect("database/database_db_files/database.db")
    cursor = conn.cursor()

    # XLSX-Datei öffnen
    wb = openpyxl.load_workbook(xlsx_file)
    sheet = wb.active

    # Durchlaufen der Zeilen in der XLSX-Datei
    for row in sheet.iter_rows(values_only=True):
        ticker_with_suffix = row[1] + "-USD"
        name = row[2]
        asset_type = "crypto"

        # Überprüfen, ob der Ticker bereits in der Datenbank existiert
        cursor.execute("SELECT COUNT(*) FROM Assets WHERE ticker=?", (ticker_with_suffix,))
        count = cursor.fetchone()[0]

        if count == 0:
            # Datensatz in die Tabelle "Assets" einfügen
            cursor.execute("INSERT INTO Assets (ticker, name, sector, type) VALUES (?, ?, ?, ?)",
                        (ticker_with_suffix, name, "", asset_type))

    # Änderungen in der Datenbank speichern
    conn.commit()

    # Verbindung zur Datenbank schließen
    conn.close()

    print("Import wurde abgeschlossen")

_insert_crypto()