from api.base_api import BaseAPI


class CourierAPI(BaseAPI):
    CREATE_ENDPOINT = "/api/v1/courier"
    LOGIN_ENDPOINT = "/api/v1/courier/login"
    DELETE_ENDPOINT = "/api/v1/courier/{courier_id}"

    @classmethod
    def create_courier(cls, payload):
        return cls._make_request("POST", cls.CREATE_ENDPOINT, json=payload)

    @classmethod
    def login_courier(cls, payload):
        return cls._make_request("POST", cls.LOGIN_ENDPOINT, json=payload)

    @classmethod
    def delete_courier(cls, courier_id):
        endpoint = cls.DELETE_ENDPOINT.format(courier_id=courier_id)
        return cls._make_request("DELETE", endpoint)