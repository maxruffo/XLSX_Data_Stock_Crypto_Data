from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

index_name = "dow_jones"
url = "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"
output_folder = "data/~index_ticker_list"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"class": "wikitable sortable"})
    table_data = []
    for row in table.find_all("tr"):
        row_data = [cell.text.strip() for cell in row.find_all(["th", "td"])]
        table_data.append(row_data)
    headers = table_data[0]
    rows = table_data[1:]
    df = pd.DataFrame(rows, columns=headers)
    
    # Vertausche die Spalten "Company" und "Ticker" und ändere die Reihenfolge der Spalten
    df = df[['Symbol', 'Company', 'Date added', 'Exchange']]
    df.columns = ['Ticker', 'Company', 'Date added', 'Exchange']  # Umbenennen der Spalten
    
    # Erstellen des Ordners, falls er nicht existiert
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_file = os.path.join(output_folder, f"{index_name}_tickers.xlsx")
    df.to_excel(output_file, index=False)
    print(f"Die XLSX-Datei wurde erfolgreich unter '{output_file}' erstellt.")
else:
    print(f"Anfrage fehlgeschlagen mit Status-Code {response.status_code}")
