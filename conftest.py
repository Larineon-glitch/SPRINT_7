import pytest

from api.courier_api import CourierAPI
from api.order_api import OrderAPI
from helpers import CourierHelper
from data import OrderData


@pytest.fixture(autouse=True)
def clean_db():
    # Очистка базы данных перед тестом (удаление всех тестовых курьеров) 
    pass


@pytest.fixture
def create_courier_and_login():
    # Фикстура создает курьера, логинит его и возвращает id, логин, пароль и имя 
    login, password, first_name = CourierHelper.register_new_courier_and_return_login_password()
    if login and password:
        login_payload = {"login": login, "password": password}
        response = CourierAPI.login_courier(login_payload)
        courier_id = response.json().get("id") if response.status_code == 200 else None
        yield login, password, first_name, courier_id

        # Удаление курьера после теста для исключения возможной ошибки о создании курьера
        if courier_id:
            CourierAPI.delete_courier(courier_id)


@pytest.fixture
def create_order_and_return_track():
    # Фикстура создает заказ и возвращает его track номер 
    payload = {
        "firstName": OrderData.ORDER_FIELDS["firstName"],
        "lastName": OrderData.ORDER_FIELDS["lastName"],
        "address": OrderData.ORDER_FIELDS["address"],
        "metroStation": OrderData.ORDER_FIELDS["metroStation"],
        "phone": OrderData.ORDER_FIELDS["phone"],
        "rentTime": OrderData.ORDER_FIELDS["rentTime"],
        "deliveryDate": OrderData.ORDER_FIELDS["deliveryDate"],
        "comment": OrderData.ORDER_FIELDS["comment"],
        "color": ["BLACK"],
    }

    response = OrderAPI.create_order(payload)
    track = response.json().get("track") if response.status_code == 201 else None
    yield track


@pytest.fixture
def create_order_and_get_id():
    # Фикстура создает заказ и возвращает его order_id 
    payload = {
        "firstName": OrderData.ORDER_FIELDS["firstName"],
        "lastName": OrderData.ORDER_FIELDS["lastName"],
        "address": OrderData.ORDER_FIELDS["address"],
        "metroStation": OrderData.ORDER_FIELDS["metroStation"],
        "phone": OrderData.ORDER_FIELDS["phone"],
        "rentTime": OrderData.ORDER_FIELDS["rentTime"],
        "deliveryDate": OrderData.ORDER_FIELDS["deliveryDate"],
        "comment": OrderData.ORDER_FIELDS["comment"],
        "color": ["BLACK"],
    }

    response = OrderAPI.create_order(payload)
    track = response.json().get("track") if response.status_code == 201 else None

    if track:
        order_response = OrderAPI.get_order_by_track(params={"t": track})
        if order_response.status_code == 200:
            order_data = order_response.json().get("order")
            if order_data:
                yield order_data.get("id")
                # Отмена заказа после теста
                OrderAPI.cancel_order(params={"track": track})
                return
    yield None