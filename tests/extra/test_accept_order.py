import allure
import pytest

from api.order_api import OrderAPI
from api.courier_api import CourierAPI
from helpers import CourierHelper


@allure.feature("Принятие заказа")
class TestAcceptOrder:

    @allure.title("Успешный запрос возвращает {{ok:true}}")
    def test_accept_order_success(self, create_order_and_get_id):
        order_id = create_order_and_get_id
        if not order_id:
            allure.skip("Заказ не был создан")

        login = CourierHelper.generate_unique_login()
        password = CourierHelper.generate_random_string(10)
        first_name = CourierHelper.generate_random_string(10)

        create_payload = {
            "login": login,
            "password": password,
            "firstName": first_name,
        }
        create_response = CourierAPI.create_courier(create_payload)
        assert create_response.status_code == 201

        login_response = CourierAPI.login_courier({"login": login, "password": password})
        courier_id = login_response.json().get("id")

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
        login = CourierHelper.generate_unique_login()
        password = CourierHelper.generate_random_string(10)
        first_name = CourierHelper.generate_random_string(10)

        create_payload = {
            "login": login,
            "password": password,
            "firstName": first_name,
        }
        create_response = CourierAPI.create_courier(create_payload)
        assert create_response.status_code == 201

        login_response = CourierAPI.login_courier({"login": login, "password": password})
        courier_id = login_response.json().get("id")

        params = {"courierId": courier_id}
        response = OrderAPI.accept_order("", params=params)        
        assert response.status_code in [400, 404], f"Ожидался 400 или 404, получен {response.status_code}"

        CourierAPI.delete_courier(courier_id)

    @allure.title("Если не передать id заказа, запрос возвращает ошибку")
    def test_accept_order_without_order_id(self):
            login = CourierHelper.generate_unique_login()
            password = CourierHelper.generate_random_string(10)
            first_name = CourierHelper.generate_random_string(10)

            create_payload = {
                "login": login,
                "password": password,
                "firstName": first_name,
            }
            create_response = CourierAPI.create_courier(create_payload)
            assert create_response.status_code == 201

            login_response = CourierAPI.login_courier({"login": login, "password": password})
            courier_id = login_response.json().get("id")

            params = {"courierId": courier_id}
            response = OrderAPI.accept_order("", params=params)
            
            assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"

            CourierAPI.delete_courier(courier_id)