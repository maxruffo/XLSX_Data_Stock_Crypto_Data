from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

index_name = "nasdaq_100"
url = "https://en.wikipedia.org/wiki/Nasdaq-100"
output_folder = f"data/~index_ticker_list"

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
    df_swapped = df[['Ticker', 'Company']]  # Vertausche die Spalten "Company" und "Ticker"
    
    # Erstellen des Ordners, falls er nicht existiert
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_file = os.path.join(output_folder, f"{index_name}_tickers.xlsx")
    with pd.ExcelWriter(output_file) as writer:
        df.to_excel(writer, sheet_name='Original', index=False)  # Speichere die Originaltabelle
        df_swapped.to_excel(writer, sheet_name='Vertauscht', index=False)  # Speichere die vertauschte Tabelle
    print(f"Die XLSX-Datei wurde erfolgreich unter '{output_file}' erstellt.")
else:
    print(f"Anfrage fehlgeschlagen mit Status-Code {response.status_code}")
