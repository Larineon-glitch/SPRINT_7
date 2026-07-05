import requests
from config import BASE_URL


class BaseAPI:
    BASE_URL = BASE_URL

    @staticmethod
    def _make_request(method, endpoint, **kwargs):
        url = f"{BaseAPI.BASE_URL}{endpoint}"
        response = requests.request(method, url, **kwargs)
        return response