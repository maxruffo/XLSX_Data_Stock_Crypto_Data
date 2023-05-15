from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

index_name = "nasdaq_100"
url = "https://en.wikipedia.org/wiki/Nasdaq-100"
output_folder = "data/stocks/~index_ticker_list/usa"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "constituents"})
    table_data = []
    for row in table.find_all("tr"):
        row_data = []
        for cell in row.find_all(["th", "td"]):
            row_data.append(cell.text.strip())
        table_data.append(row_data)
    headers = table_data[0]
    rows = table_data[1:]
    df = pd.DataFrame(rows, columns=headers)
    
    # Ändere die Namen der Spalten
    df = df.rename(columns={"GICS Sector": "Sector", "GICS Sub-Industry": "Sub-Sector"})
    
    # Ändere die Reihenfolge der Spalten
    df = df[['Ticker', 'Company', 'Sector', 'Sub-Sector']]
    
    # Erstellen des Ordners, falls er nicht existiert
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_file = os.path.join(output_folder, f"{index_name}_tickers.xlsx")
    df.to_excel(output_file, index=False)
    print(f"Die XLSX-Datei wurde erfolgreich unter '{output_file}' erstellt.")
else:
    print(f"Anfrage fehlgeschlagen mit Status-Code {response.status_code}")
