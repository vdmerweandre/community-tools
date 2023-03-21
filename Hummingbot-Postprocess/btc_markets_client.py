import base64
import hashlib
import hmac
import time

from base_rest_api import BaseRestApi
import btc_markets_constants as CONSTANTS


class BtcMarketsClient(BaseRestApi):
    """
    Auth class required by btc_markets API
    Learn more at https://api.btcmarkets.net/doc/v3#section/Authentication/Authentication-process
    """
    def __init__(self, url):
        super().__init__(url=url)

    @staticmethod
    def check_response_data(response_data):
        if response_data.status_code == 200:
            try:
                data = response_data.json()
            except ValueError:
                raise Exception(-1, response_data.content)
            else:
                if data and "code" in data:
                    if data.get("code") == 0:
                        if "data" in data:
                            return data["data"]
                        else:
                            return data
                    else:
                        raise Exception(response_data.status_code, response_data.text)
                else:
                    return data
        else:
            raise Exception(response_data.status_code, response_data.text)

    def get_ticker(self, symbol, **kwargs):
        params = {}
        if kwargs:
            params.update(kwargs)
        path = CONSTANTS.TICKER_URL+f"/{symbol}/ticker"

        return self._request("GET", path, params=params, auth=False)

    def get_candlesticks(self, marketId, timeframe, start, end, limit, **kwargs):
        params = {"timeWindow": timeframe, "from": start, "to": end, "limit": limit, }
        if kwargs:
            params.update(kwargs)
        print(f"params: {params}")
        path = CONSTANTS.CANDLESTICK_URL.replace('#marketId#', marketId)

        return self._request("GET", path, params=params, auth=False)
    
    def list_asset(self, **kwargs):
        params = {}
        if kwargs:
            params.update(kwargs)
        return self._request("GET", CONSTANTS.MARKETS_URL, params=params, auth=False)
    
    def _timestamp_in_milliseconds(self) -> int:
        return int(self._time() * 1e3)

    def _time(self):
        return time.time()