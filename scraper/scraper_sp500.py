from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
output_folder = "data/~index_ticker_list"

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
    headers[0] = "Ticker"  # Umbenennen der Spalte von "Symbol" zu "Ticker"
    rows = table_data[1:]
    df = pd.DataFrame(rows, columns=headers)
    
    # Erstellen des Ordners, falls er nicht existiert
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_file = os.path.join(output_folder, "sp_500_tickers.xlsx")
    df.to_excel(output_file, index=False)
    print(f"Die XLSX-Datei wurde erfolgreich unter '{output_file}' erstellt.")
else:
    print(f"Anfrage fehlgeschlagen mit Status-Code {response.status_code}")
