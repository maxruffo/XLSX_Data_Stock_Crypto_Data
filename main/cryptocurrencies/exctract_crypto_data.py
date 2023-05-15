import os
import pandas as pd
import yfinance as yf
from datetime import datetime

data_folder = "data/cryptocurrencies"
target_folder = "data/cryptocurrencies"

# Durchlaufen der Ordner in "data/~index_ticker_list/"




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




ticker_set = extract_tickers()

for crypto in ticker_set:
    try:
        # Überprüfen, ob das DataFrame leer ist
        data = yf.download(crypto, period='1d', interval='1m', progress=False)
        if data.empty:
            # Datenframe ist leer, speichern des Tickersymbols in einer separaten xlsx-Datei
            error_folder = "errors/runtime"
            if not os.path.exists(error_folder):
                os.makedirs(error_folder)
            error_file = os.path.join(error_folder, "not_found_crypto.xlsx")
            not_found_df = pd.DataFrame({'Ticker': [crypto]})
            if os.path.exists(error_file):
                # Falls die Datei bereits existiert, die neue Zeile hinzufügen
                existing_data = pd.read_excel(error_file)
                updated_data = pd.concat([existing_data, not_found_df])
                updated_data.to_excel(error_file, index=False)
            else:
                # Falls die Datei noch nicht existiert, eine neue Datei erstellen
                not_found_df.to_excel(error_file, index=False)
            print(f"Das DataFrame für {crypto} ist leer. Tickersymbol wurde in '{error_file}' hinzugefügt.")
           
            continue
           

        # Ordner für die jeweilige Aktie erstellen
        crypto_folder = os.path.join(target_folder, crypto)
        if not os.path.exists(crypto_folder):
            os.makedirs(crypto_folder)

        # Dateiname für den aktuellen Tag erstellen
        current_date = datetime.today().strftime('%Y-%m-%d')
        current_filename = os.path.join(crypto_folder, f"{crypto}.csv")

        if os.path.exists(current_filename):
            # Daten für den aktuellen Tag bereits vorhanden, aktualisieren
            data.to_csv(current_filename, mode='a', header=False)
            print(f"Aktualisierte Daten für {crypto} wurden in {current_filename} gespeichert.")
        else:
            # Daten für den aktuellen Tag herunterladen und speichern
            data.to_csv(current_filename)
            print(f"Daten für {crypto} wurden in {current_filename} gespeichert.")

        # Ordner für die historischen Daten der Aktie erstellen
        crypto_history_folder = os.path.join(crypto_folder, "history")
        if not os.path.exists(crypto_history_folder):
            os.makedirs(crypto_history_folder)

        # Daten für den aktuellen Tag in den historischen Ordner der Aktie kopieren
        crypto_history_filename = os.path.join(crypto_history_folder, f"{current_date}.csv")
        data.to_csv(crypto_history_filename)
        print(f"Daten für {crypto} wurden in {crypto_history_filename} (historischer Ordner) gespeichert.")
        print("\n")
    except Exception as e:
        print(f"Fehler beim Herunterladen der Daten für {crypto}: {str(e)}")