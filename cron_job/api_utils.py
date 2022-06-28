import logging
from urllib.parse import urljoin

import requests


class APIRequest:
    def __init__(self, host, path):
        self.host = host
        self.path = path
        self.url = urljoin(host, path)

    def request(self, method, params=None, headers=None, data=None):
        try:
            response = getattr(requests, method.lower())(
                self.url, params=params, headers=headers, data=data
            )
        except Exception as e:
            logging.error(e)
            raise

        if response.ok:
            return response.json()
        else:
            logging.error(response.text)
            raise
