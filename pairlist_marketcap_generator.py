#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# --- ↑↓ Do not remove these libs ↑↓ -----------------------------------------------------------------------------------
import argparse
import json
import time
import re

import requests
# ---- ↑ Do not remove these libs ↑ ------------------------------------------------------------------------------------

# Binance All Tradable Pairs Retriever with Market Cap
# ====================================================
__author__ = 'PoCk3T & Rikj000 + aLca'
__copyright__ = 'The GNU General Public License v3.0'
exchange_info_url = 'https://api2.binance.com/api/v3/exchangeInfo'
ticker_url = 'https://api2.binance.com/api/v3/ticker/24hr?symbol={}'

def get_market_cap(pair):
    """Returns the market capitalization of the given trading pair on Binance."""
    # Remove any illegal characters from the pair symbol
    pair = re.sub(r'[^A-Z0-9-_.]', '', pair)

    ticker_resp = requests.get(url=ticker_url.format(pair))
    ticker_data = ticker_resp.json()
    # print(ticker_data)  # Added for troubleshooting
    return float(ticker_data['quoteVolume'])

def main():
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Binance All Tradable Pairs Retriever with Market Cap')
    parser.add_argument('-q', '--quote',
                        help=f'<Optional> Quote of the Binance pairs to retrieve (example, use "BTC" to retrieve all '
                             f'pairs like ADA/BTC, ETH/BTC, etc..); default is USDT', required=False, default='USDT')
    parser.add_argument('-n', '--number',
                        help='<Optional> Number of top pairs to retrieve; default is 10', required=False, type=int, default=10)
    args = parser.parse_args()
    currency = args.quote
    num_pairs = args.number

    # Retrieve the list of all trading pairs on Binance
    resp = requests.get(url=exchange_info_url)
    data = resp.json()

    # Filter the trading pairs by quote currency, status, and trading type
    pairs_with_given_quote = ['/{}'.format(currency).join(str(d['symbol']).rsplit(currency, 1)) for d in data['symbols']
                              if d['quoteAsset'] == currency
                              and d['status'] == 'TRADING'
                              and d['isSpotTradingAllowed'] is True
                              and d['isMarginTradingAllowed'] is True
                              ]

    # Retrieve the market capitalization of each trading pair
    pairs_with_cap = []
    for pair in pairs_with_given_quote:
        market_cap = get_market_cap(pair)
        pairs_with_cap.append((pair, market_cap))
        time.sleep(0.1)  # To avoid overloading the Binance API

    # Sort the pairs by market capitalization and retrieve the top N pairs
    top_pairs = sorted(pairs_with_cap, key=lambda x: x[1], reverse=True)[:num_pairs]
    top_pairs = [pair[0] for pair in top_pairs]

    # Print the list of top N pairs
    print(json.dumps(top_pairs, indent=4, sort_keys=True))


if __name__ == '__main__':
    main()