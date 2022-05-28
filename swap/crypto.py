import os
from inspect import getcallargs

from coinbase.wallet.client import Client
from coinbase.wallet.error import NotFoundError


def get_current_value(symbol):
    client = Client(os.environ.get("CBK"), os.environ.get("CBS"))
    try:
        res = client.get_buy_price(currency_pair=f"{symbol}-USD")
    except NotFoundError as e:
        return None
    return float(res.get("amount"))
