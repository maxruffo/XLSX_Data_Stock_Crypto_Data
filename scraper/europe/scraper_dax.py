from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

index_name = "dax"
url = "https://en.wikipedia.org/wiki/DAX"
output_folder = "data/~index_ticker_list/europe"

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
    
    # Ändere die Reihenfolge der Spalten
    df = df[['Ticker', 'Company', 'Prime Standard Sector','Employees', 'Founded']]
    
    # Umbenennen der Spalte "Prime Standard Sector" in "Sector"
    df = df.rename(columns={"Prime Standard Sector": "Sector"})
    
    
    
    # Erstellen des Ordners, falls er nicht existiert
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_file = os.path.join(output_folder, f"{index_name}_tickers.xlsx")
    df.to_excel(output_file, index=False)
    print(f"Die XLSX-Datei wurde erfolgreich unter '{output_file}' erstellt.")
else:
    print(f"Anfrage fehlgeschlagen mit Status-Code {response.status_code}")
