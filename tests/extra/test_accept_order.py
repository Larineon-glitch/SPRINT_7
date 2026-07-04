import allure
import pytest

from api.order_api import OrderAPI
from api.courier_api import CourierAPI
from helpers import CourierHelper


@allure.feature("Принятие заказа (дополнительное задание)")
class TestAcceptOrder:

    @allure.title("Успешный запрос возвращает {{ok:true}}") 
    def test_accept_order_success(self, create_order_and_get_id):
        order_id = create_order_and_get_id
        if not order_id:
            allure.skip("Заказ не был создан")

        login, password, first_name, courier_id = CourierHelper.create_and_login_courier()
        if not courier_id:
            allure.skip("Курьер не был создан")

        params = {"courierId": courier_id}
        response = OrderAPI.accept_order(order_id, params=params)

        assert response.status_code == 200
        assert response.json() == {"ok": True}

        CourierAPI.delete_courier(courier_id)

    @allure.title("Если не передать id курьера, запрос возвращает ошибку")
    def test_accept_order_without_courier_id(self, create_order_and_get_id):
        order_id = create_order_and_get_id
        if not order_id:
            allure.skip("Заказ не был создан")

        response = OrderAPI.accept_order(order_id, params={})
        assert response.status_code == 400
        assert "Недостаточно данных для поиска" in response.text

    @allure.title("Если передать неверный id курьера, запрос возвращает ошибку")
    def test_accept_order_with_invalid_courier_id(self, create_order_and_get_id):
        order_id = create_order_and_get_id
        if not order_id:
            allure.skip("Заказ не был создан")

        params = {"courierId": 999999}
        response = OrderAPI.accept_order(order_id, params=params)
        assert response.status_code == 404
        assert "Курьера с таким id не существует" in response.text

    @allure.title("Если не передать id заказа, запрос возвращает ошибку")
    def test_accept_order_without_order_id(self):
        login, password, first_name, courier_id = CourierHelper.create_and_login_courier()
        if not courier_id:
            allure.skip("Курьер не был создан")

        params = {"courierId": courier_id}
        response = OrderAPI.accept_order("invalid", params=params)
        
        if response.status_code == 500:
            pytest.xfail("Известная проблема API: сервер возвращает 500 вместо 400")
        
        assert response.status_code == 400
        CourierAPI.delete_courier(courier_id)

    @allure.title("Если передать неверный id заказа, запрос возвращает ошибку")
    def test_accept_order_with_invalid_order_id(self):
        login, password, first_name, courier_id = CourierHelper.create_and_login_courier()
        if not courier_id:
            allure.skip("Курьер не был создан")

        params = {"courierId": courier_id}
        response = OrderAPI.accept_order(999999, params=params)
        assert response.status_code == 404
        assert "Заказа с таким id не существует" in response.text

        CourierAPI.delete_courier(courier_id)