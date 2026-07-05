import allure
import pytest

from api.courier_api import CourierAPI
from helpers import CourierHelper


@allure.feature("Удаление курьера")
class TestDeleteCourier:
    @allure.title("Неуспешный запрос возвращает ошибку")
    def test_delete_courier_fails_without_id(self):
        response = CourierAPI.delete_courier("")
        assert response.status_code == 404
        assert "Not Found" in response.text

    @allure.title("Успешный запрос возвращает {{ok:true}}")
    def test_delete_courier_success(self):
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

        response = CourierAPI.delete_courier(courier_id)
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Запрос без id возвращает ошибку")
    def test_delete_courier_without_id(self):
        response = CourierAPI.delete_courier("")
        assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"

    @allure.title("Запрос с несуществующим id возвращает ошибку")
    def test_delete_courier_nonexistent_id(self):
        response = CourierAPI.delete_courier(999999)
        assert response.status_code == 404

        response_data = response.json()
        assert "message" in response_data
        assert "Курьера с таким id нет" in response_data.get("message", "")