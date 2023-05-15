from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

url = "https://en.wikipedia.org/wiki/FTSE_100_Index"
output_folder = "data/stocks/~index_ticker_list/europe"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "constituents"})
    table_data = []
    for row in table.find_all("tr"):
        row_data = [cell.text.strip() for cell in row.find_all(["th", "td"])]
        table_data.append(row_data)
    headers = table_data[0]
    headers[0], headers[1], headers[2] = headers[1], headers[0], headers[2]  # Spaltenreihenfolge ändern
    headers[2] = "Sector"  # Umbenennen der Spalte "FSTE Industry" zu "Sector"
    rows = table_data[1:]
    df = pd.DataFrame(rows, columns=headers)
    
    # Vertausche die Spalten "Company" und "Ticker"
    df[['Company', 'Ticker']] = df[['Ticker', 'Company']]
    
    # Erstellen des Ordners, falls er nicht existiert
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_file = os.path.join(output_folder, "ftse_100_tickers.xlsx")
    df.to_excel(output_file, index=False)
    print(f"Die vollständige Tabelle wurde erfolgreich unter '{output_file}' als XLSX-Datei erstellt.")
else:
    print(f"Anfrage fehlgeschlagen mit Status-Code {response.status_code}")
