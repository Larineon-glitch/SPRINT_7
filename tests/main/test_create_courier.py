import allure
import pytest

from api.courier_api import CourierAPI
from data import CourierData
from helpers import CourierHelper


@allure.feature("Создание курьера")
class TestCreateCourier:
    @allure.title("Курьера можно создать")
    def test_create_courier_success(self):
        login = CourierHelper.generate_unique_login()
        password = CourierHelper.generate_random_string(10)
        first_name = CourierHelper.generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name,
        }

        response = CourierAPI.create_courier(payload)
        assert response.status_code == 201
        assert response.json() == {"ok": True}

        login_response = CourierAPI.login_courier({"login": login, "password": password})
        courier_id = login_response.json().get("id")
        CourierAPI.delete_courier(courier_id)

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier(self):
        login = CourierHelper.generate_unique_login()
        password = CourierHelper.generate_random_string(10)
        first_name = CourierHelper.generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name,
        }

        response1 = CourierAPI.create_courier(payload)
        assert response1.status_code == 201
        assert response1.json() == {"ok": True}

        response2 = CourierAPI.create_courier(payload)
        assert response2.status_code == 409
        assert response2.json().get("message") == CourierData.INVALID_LOGIN_MESSAGES["duplicate_login"]

        login_response = CourierAPI.login_courier({"login": login, "password": password})
        courier_id = login_response.json().get("id")
        CourierAPI.delete_courier(courier_id)

    @allure.title("Для создания курьера нужно передать все обязательные поля")
    @pytest.mark.parametrize("missing_field", ["login", "password", "firstName"])
    def test_create_courier_missing_field(self, missing_field):
        payload = {
            "login": CourierHelper.generate_unique_login(),
            "password": CourierHelper.generate_random_string(10),
            "firstName": CourierHelper.generate_random_string(10),
        }
        del payload[missing_field]

        response = CourierAPI.create_courier(payload)        
        if missing_field == "firstName":
            assert response.status_code == 201, f"Ожидался 201, получен {response.status_code}"
            assert response.json() == {"ok": True}
            
            login_response = CourierAPI.login_courier({"login": payload["login"], "password": payload["password"]})
            courier_id = login_response.json().get("id")
            CourierAPI.delete_courier(courier_id)
        else:
            assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
            assert response.json().get("message") == CourierData.INVALID_LOGIN_MESSAGES["missing_login"]

    @allure.title("Успешный запрос возвращает {{ok:true}}")
    def test_create_courier_returns_ok(self):
        login = CourierHelper.generate_unique_login()
        password = CourierHelper.generate_random_string(10)
        first_name = CourierHelper.generate_random_string(10)

        payload = {"login": login, "password": password, "firstName": first_name}
        response = CourierAPI.create_courier(payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

        login_response = CourierAPI.login_courier({"login": login, "password": password})
        courier_id = login_response.json().get("id")
        CourierAPI.delete_courier(courier_id)

    @allure.title("Создание курьера с существующим логином возвращает ошибку")
    def test_create_courier_with_existing_login(self):
        login = CourierHelper.generate_unique_login()
        password = CourierHelper.generate_random_string(10)
        first_name = CourierHelper.generate_random_string(10)

        payload1 = {
            "login": login,
            "password": password,
            "firstName": first_name,
        }
        response1 = CourierAPI.create_courier(payload1)
        assert response1.status_code == 201

        payload2 = {
            "login": login,
            "password": CourierHelper.generate_random_string(10),
            "firstName": CourierHelper.generate_random_string(10),
        }
        response2 = CourierAPI.create_courier(payload2)

        assert response2.status_code == 409
        assert response2.json().get("message") == CourierData.INVALID_LOGIN_MESSAGES["duplicate_login"]

        login_response = CourierAPI.login_courier({"login": login, "password": password})
        courier_id = login_response.json().get("id")
        CourierAPI.delete_courier(courier_id)