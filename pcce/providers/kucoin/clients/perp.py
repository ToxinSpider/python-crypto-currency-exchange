import base64
import hashlib
import hmac
import json
import time
from typing import Optional

import requests
from pcce.providers.kucoin.exceptions import KucoinAPIException, KucoinRequestException
from pcce.providers.kucoin.orders import LimitOrder, MarketOrder


class Client:
    API_URL = "https://api-futures.kucoin.com"
    API_V1 = "v1"

    DEFAULT_HEADERS = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    def __init__(self, api_key, api_secret, passphrase):
        """Kucoin API Client constructor

        https://docs.kucoin.com/

        :param api_key: Api Token Id
        :type api_key: string
        :param api_secret: Api Secret
        :type api_secret: string
        :param passphrase: Api Passphrase used to create API
        :type passphrase: string
        """
        self.API_KEY = api_key
        self.API_SECRET = api_secret
        self.API_PASSPHRASE = passphrase

    @staticmethod
    def _handle_response(response):
        """Internal helper for handling API responses from the Kucoin server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """

        if not str(response.status_code).startswith('2'):
            raise KucoinAPIException(response)
        try:
            res = response.json()

            if 'code' in res and res['code'] != "200000":
                raise KucoinAPIException(response)

            if 'success' in res and not res['success']:
                raise KucoinAPIException(response)

            # by default return full response
            # if it's a normal response we have a data attribute, return that
            if 'data' in res:
                res = res['data']
            return res
        except ValueError:
            raise KucoinRequestException(f'Invalid Response: {response.text}')

    def _create_path(self, path, api_version=None):
        api_version = api_version or self.API_V1
        return f'/api/{api_version}/{path}'

    def _create_url(self, path):
        return f'{self.API_URL}{path}'

    def _generate_signature(
        self,
        nonce: str,
        method: str,
        api_path: str,
        data: str
    ) -> bytes:
        str_to_sign = f"{nonce}{method}{api_path}{data}"
        signature = base64.b64encode(
            hmac.new(
                self.API_SECRET.encode('utf-8'),
                str_to_sign.encode('utf-8'),
                hashlib.sha256
            ).digest()
        )
        return signature

    def _generate_passphrase(self) -> bytes:
        return base64.b64encode(
            hmac.new(
                self.API_SECRET.encode('utf-8'),
                self.API_PASSPHRASE.encode('utf-8'),
                hashlib.sha256
            ).digest()
        )

    def _request(self, method: str, path: str, api_version: Optional[str] = None, **kwargs) -> dict:
        # set default requests timeout
        data = kwargs.get('data', {})
        headers = kwargs.get('headers', self.DEFAULT_HEADERS)

        data = json.dumps(data)

        full_path = self._create_path(path, api_version)
        url = self._create_url(full_path)

        # generate signature
        nonce = int(time.time() * 1000)
        headers['KC-API-TIMESTAMP'] = str(nonce)
        headers['KC-API-SIGN'] = self._generate_signature(
            nonce, method, full_path, data)
        headers['KC-API-KEY'] = self.API_KEY
        headers['KC-API-PASSPHRASE'] = self._generate_passphrase()
        headers['KC-API-KEY-VERSION'] = "2"

        response = requests.request(
            method=method,
            url=url,
            data=data,
            headers=headers
        )
        return self._handle_response(response)

    def create_limit_order(
        self,
        order: LimitOrder
    ) -> dict:
        return self._request("POST", "orders", data=order.as_dict())

    def create_market_order(
        self,
        order: MarketOrder
    ) -> dict:
        return self._request("POST", "orders", data=order.as_dict())
