import sqlite3
import os
import pandas as pd

# Ordner erstellen, falls er nicht existiert
if not os.path.exists('database'):
    os.makedirs('database')

# Verbindung zur Datenbank herstellen (oder erstellen, wenn sie noch nicht existiert)
conn = sqlite3.connect('database/database.db')

# Cursor-Objekt erstellen, um die Datenbankabfragen auszuführen
cursor = conn.cursor()

# Tabelle für Aktien-Ticker erstellen
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tickers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        name TEXT NOT NULL,
        sector TEXT
    )
''')

# Tabelle für Aktien-Kursdaten erstellen
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pricedata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker_id INTEGER NOT NULL,
        date DATE NOT NULL,
        open REAL NOT NULL,
        high REAL NOT NULL,
        low REAL NOT NULL,
        close REAL NOT NULL,
        adj_close REAL NOT NULL,
        volume INTEGER NOT NULL,
        FOREIGN KEY (ticker_id) REFERENCES stocks(id)
    )
''')




