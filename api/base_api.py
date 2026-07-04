import requests


class BaseAPI:
    BASE_URL = "https://qa-scooter.praktikum-services.ru"

    @staticmethod
    def _make_request(method, endpoint, **kwargs):
        url = f"{BaseAPI.BASE_URL}{endpoint}"
        response = requests.request(method, url, **kwargs)
        return response