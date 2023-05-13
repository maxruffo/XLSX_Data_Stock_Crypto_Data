import sys
import yfinance as yf
import pandas as pd

# Ticker-Symbol angeben
ticker_symbol = "AMC"  # ".PA" steht für die Börse Euronext Paris

# DataFrame für die Daten initialisieren
data = None

# Variable zum Speichern des gedruckten Outputs
terminal_output = ""

# Umlenken des Standard-Outputs
class OutputCatcher:
    def write(self, text):
        global terminal_output
        terminal_output += text

sys.stdout = OutputCatcher()

try:
    # Versuche, die Daten mit yfinance herunterzuladen
    data = yf.download(ticker_symbol, period="1d", interval="1m")
    
except Exception as e:
    # Fehlermeldung anzeigen
    print(str(e))

finally:
    # Standard-Output wiederherstellen
    sys.stdout = sys.__stdout__

    # Terminal-Output in log.xlsx speichern
    log_data = pd.DataFrame({"Terminal Output": [terminal_output]})
    print(terminal_output)
    log_data.to_excel("log.xlsx", index=False)
