
# Impotierung der Module für die Index Datei erstellung
from collector.scraper.stocks.stock_scraper import _run_stocks
from collector.scraper.cryptocurrencies.crypto_scraper import _run_crypto

# Importierung der Module für die Sammlung der Daten
from collector.exctract_data.cryptocurrencies.exctract_crypto_data import _run_crypto_extractor
from collector.exctract_data.stocks.exctract_stock_data import _run_stock_extractor

# Erstellung der index Datein
def run_scraper():
    _run_crypto()
    _run_stocks()

def run_extractor():
    _run_crypto_extractor()
    _run_stock_extractor()
    

run_extractor()

