from api.base_api import BaseAPI


class OrderAPI(BaseAPI):
    CREATE_ENDPOINT = "/api/v1/orders"
    GET_ORDERS_LIST_ENDPOINT = "/api/v1/orders"
    ACCEPT_ORDER_ENDPOINT = "/api/v1/orders/accept/{order_id}"
    GET_ORDER_BY_TRACK_ENDPOINT = "/api/v1/orders/track"
    CANCEL_ORDER_ENDPOINT = "/api/v1/orders/cancel"

    @classmethod
    def create_order(cls, payload):
        return cls._make_request("POST", cls.CREATE_ENDPOINT, json=payload)

    @classmethod
    def get_orders_list(cls, params=None):
        return cls._make_request("GET", cls.GET_ORDERS_LIST_ENDPOINT, params=params)

    @classmethod
    def accept_order(cls, order_id, params):
        endpoint = cls.ACCEPT_ORDER_ENDPOINT.format(order_id=order_id)
        return cls._make_request("PUT", endpoint, params=params)

    @classmethod
    def get_order_by_track(cls, params):
        return cls._make_request("GET", cls.GET_ORDER_BY_TRACK_ENDPOINT, params=params)

    @classmethod
    def cancel_order(cls, params):
        return cls._make_request("PUT", cls.CANCEL_ORDER_ENDPOINT, params=params)