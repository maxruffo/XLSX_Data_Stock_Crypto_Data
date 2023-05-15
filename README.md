# Yahoo Finance Data Downloader

This program is designed to download daily minute data from Yahoo Finance for all stocks in major stock indices and price data for the top 50 cryptocurrencies.

In the Folder "data" you can find all the data that is collected.
The data folder is build like this:

```sh
- data
    - cryptocurrencies
        - ADA-USD
            - history
                - 2023-05-15.csv
                - 2023-05-16.csv
            - ADA-USD.csv #concat of all the data in the history folder 
        - ~index_cryptocurrencies_list.xlsx # Top 50 Cryptocurrencies
        - ALGO-USD
        - APE-USD
        - APT-USD
        - ARB-USD
        - ...
    - stocks
        - ~index_ticker_list
            - eruope
                - cac_40_tickers.xlsx #ticker list of the cac40
                - dax_tickers.xlsx
                - ftse_100_tickers.xlsx
            - usa
            - asia # to-do
        - 1COV.DE
            - history
                - 2023-05-15.xlsx
            - 1COV.DE.csv # concat of all the data in the history folder
        - A
        - AAL
        - AAP
        - AAPL
        - ...
```

## Prerequisites

Before running the program, make sure you have the following dependencies installed:

- Python (version 3.x)
- Required Python libraries: `pandas`, `yfinance`, `requests`, `openpyxl`

You can install the required libraries by running the following command:

```sh
pip install pandas yfinance requests openpyxl
```

## Usage

1. Clone or download this repository to your local machine.
2. Open a terminal or command prompt and navigate to the project directory.
3. Run the following command to start the program:

```sh
python _main_.py
```

The program will automatically download the minute data for all stocks in major stock indices and price data for the top 50 cryptocurrencies.

4. Once the program finishes, you will find the downloaded data stored in the `data` directory.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This program is licensed under the [MIT License](LICENSE).

# To-do:

- add Asia Index Scraper
- fehlerhanlding für yfinanc

# To - do erledigt:

- github workflow funktioniert nicht
