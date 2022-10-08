# Watchlist-Converter
This script can be used to convert the exported watch lists from TradingView to a suitable format for [Dhan TradingView](https://dhan.co/).

## Requirements 
This requires python 3.6+ version.
## Installation
```
pip install pandas
```
## Run
You can run this code by running following cmd from terminal:
```
python watchlist_converter.py --file test_paper_products.txt --platform dhan
```
test_paper_products.txt is the filename of exported trading view watchlist. 

The converted watchlist will be stored as - dhan_test_paper_products.txt

## Limitations
This only supports EQ segment of NSE and BSE.
