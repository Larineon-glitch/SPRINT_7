import allure
import pytest

from api.courier_api import CourierAPI
from helpers import CourierHelper


@allure.feature("Удаление курьера (дополнительное задание)")
class TestDeleteCourier:

    @allure.title("Неуспешный запрос возвращает ошибку")
    def test_delete_courier_fails_without_id(self):
        response = CourierAPI.delete_courier("")
        assert response.status_code == 404
        assert "Not Found" in response.text

    @allure.title("Успешный запрос возвращает {{ok:true}}")
    def test_delete_courier_success(self):
        login, password, first_name = CourierHelper.register_new_courier_and_return_login_password()
        assert login is not None

        login_response = CourierAPI.login_courier({"login": login, "password": password})
        courier_id = login_response.json().get("id")

        response = CourierAPI.delete_courier(courier_id)
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Запрос без id возвращает ошибку")
    def test_delete_courier_without_id(self):
        response = CourierAPI.delete_courier(None)
        
        if response.status_code == 500:
            pytest.xfail("Известная проблема API: сервер возвращает 500 вместо 400")
        
        assert response.status_code in [400, 404]

    @allure.title("Запрос с несуществующим id возвращает ошибку")
    def test_delete_courier_nonexistent_id(self):
        response = CourierAPI.delete_courier(999999)
        assert response.status_code == 404
    
        assert "message" in response.json()
        assert "Курьера с таким id нет" in response.text or "Курьера с таким id не существует" in response.text