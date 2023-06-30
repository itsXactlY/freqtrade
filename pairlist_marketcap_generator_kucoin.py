#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import time
import re

import requests

# KuCoin All Tradable Pairs Retriever with Market Cap
# ====================================================
__author__ = 'PoCk3T & Rikj000 + aLca'
__copyright__ = 'The GNU General Public License v3.0'
exchange_info_url = 'https://api.kucoin.com/api/v1/symbols'
ticker_url = 'https://api.kucoin.com/api/v1/market/stats?symbol={}'

def get_market_cap(pair):
    """Returns the market capitalization of the given trading pair on KuCoin."""
    # Remove any illegal characters from the pair symbol
    pair = re.sub(r'[^A-Z0-9-_.]', '', pair)

    ticker_resp = requests.get(url=ticker_url.format(pair))
    ticker_data = ticker_resp.json()['data']
    # print(ticker_data)  # Added for troubleshooting
    return float(ticker_data['volValue'])

def main():
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='KuCoin All Tradable Pairs Retriever with Market Cap')
    parser.add_argument('-q', '--quote',
                        help=f'<Optional> Quote of the KuCoin pairs to retrieve (example, use "BTC" to retrieve all '
                             f'pairs like ADA-BTC, ETH-BTC, etc..); default is USDT', required=False, default='USDT')
    parser.add_argument('-n', '--number',
                        help='<Optional> Number of top pairs to retrieve; default is 10', required=False, type=int, default=10)
    args = parser.parse_args()
    currency = args.quote
    num_pairs = args.number

    # Retrieve the list of all trading pairs on KuCoin
    print('... Highly trained apes will work as fast they can - be patient ...')
    resp = requests.get(url=exchange_info_url)
    data = resp.json()

    # Filter the trading pairs by quote currency, status, and trading type
    pairs_with_given_quote = [d['symbol'] for d in data['data']
                              if d['quoteCurrency'] == currency
                              and d['enableTrading'] is True
                              ]

    # Retrieve the market capitalization of each trading pair
    pairs_with_cap = []
    for pair in pairs_with_given_quote:
        market_cap = get_market_cap(pair)
        pairs_with_cap.append((pair, market_cap))
        # time.sleep(0.025)  # To avoid overloading the KuCoin API

    # Sort the pairs by market capitalization and retrieve the top N pairs
    top_pairs = sorted(pairs_with_cap, key=lambda x: x[1], reverse=True)[:num_pairs]
    top_pairs = [pair[0] for pair in top_pairs]

    # Print the list of top N pairs
    print(json.dumps(top_pairs, indent=4, sort_keys=True))


if __name__ == '__main__':
    main()