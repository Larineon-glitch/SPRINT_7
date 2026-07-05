import allure
import pytest

from api.order_api import OrderAPI
from data import OrderData


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с разными вариантами цветов")
    @pytest.mark.parametrize("colors, color_name", OrderData.COLOR_VARIANTS)
    def test_create_order_with_colors(self, colors, color_name):
        payload = {
            "firstName": OrderData.ORDER_FIELDS["firstName"],
            "lastName": OrderData.ORDER_FIELDS["lastName"],
            "address": OrderData.ORDER_FIELDS["address"],
            "metroStation": OrderData.ORDER_FIELDS["metroStation"],
            "phone": OrderData.ORDER_FIELDS["phone"],
            "rentTime": OrderData.ORDER_FIELDS["rentTime"],
            "deliveryDate": OrderData.ORDER_FIELDS["deliveryDate"],
            "comment": OrderData.ORDER_FIELDS["comment"],
            "color": colors,
        }

        response = OrderAPI.create_order(payload)
        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)

    @allure.title("Тело ответа содержит track")
    def test_create_order_returns_track(self):
        payload = {
            "firstName": OrderData.ORDER_FIELDS["firstName"],
            "lastName": OrderData.ORDER_FIELDS["lastName"],
            "address": OrderData.ORDER_FIELDS["address"],
            "metroStation": OrderData.ORDER_FIELDS["metroStation"],
            "phone": OrderData.ORDER_FIELDS["phone"],
            "rentTime": OrderData.ORDER_FIELDS["rentTime"],
            "deliveryDate": OrderData.ORDER_FIELDS["deliveryDate"],
            "comment": OrderData.ORDER_FIELDS["comment"],
            "color": OrderData.DEFAULT_COLORS,
        }

        response = OrderAPI.create_order(payload)
        assert response.status_code == 201
        assert "track" in response.json()
        assert response.json()["track"] is not None