# File contains error handler for input data
# and get request from API


import requests
import json

from config import API_KEY, currency


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Cannot convert same currencies {base}.')

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise APIException(f'Unable to process currency {quote}')

        try:
            base_ticker = currency[base]
        except KeyError:
            raise APIException(f'Unable to process currency {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Unable to process amount {amount}')

        r = requests.get(
            f'https://free.currconv.com/api/v7/convert?q={quote_ticker}_{base_ticker}&compact=ultra&apiKey={API_KEY}')
        total_base = json.loads(r.content)[currency[quote]+'_'+currency[base]]

        return total_base, amount
