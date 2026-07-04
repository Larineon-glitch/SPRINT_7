import allure
import pytest

from api.courier_api import CourierAPI
from data import CourierData
from helpers import CourierHelper


@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Курьера можно создать")
    def test_create_courier_success(self):
        login, password, first_name = CourierHelper.register_new_courier_and_return_login_password()
        assert login is not None
        assert password is not None
        assert first_name is not None

        login_payload = {"login": login, "password": password}
        response = CourierAPI.login_courier(login_payload)
        assert response.status_code == 200
        assert "id" in response.json()

        courier_id = response.json().get("id")
        CourierAPI.delete_courier(courier_id)

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier(self):
        login, password, first_name = CourierHelper.register_new_courier_and_return_login_password()
        assert login is not None

        payload = {"login": login, "password": password, "firstName": first_name}

        # Первое создание должно быть успешным
        response1 = CourierAPI.create_courier(payload)
        assert response1.status_code == 201, f"Первое создание вернуло {response1.status_code}"
        assert response1.json() == {"ok": True}

        # Второе создание должно вернуть ошибку 409
        response2 = CourierAPI.create_courier(payload)
        assert response2.status_code == 409
        assert response2.json().get("message") == CourierData.INVALID_LOGIN_MESSAGES["duplicate_login"]

        # Удаляем созданного курьера
        login_response = CourierAPI.login_courier({"login": login, "password": password})
        courier_id = login_response.json().get("id")
        CourierAPI.delete_courier(courier_id)

    @allure.title("Для создания курьера нужно передать все обязательные поля (login и password)")
    @pytest.mark.parametrize("missing_field", ["login", "password"])  
    def test_create_courier_missing_field(self, missing_field):
        payload = {
            "login": CourierHelper.generate_random_string(10),
            "password": CourierData.DEFAULT_PASSWORD,
            "firstName": CourierData.DEFAULT_FIRST_NAME,
        }
        del payload[missing_field]

        response = CourierAPI.create_courier(payload)
        assert response.status_code == 400
        assert response.json().get("message") == CourierData.INVALID_LOGIN_MESSAGES["missing_login"]

    @allure.title("Курьера можно создать без поля firstName")
    def test_create_courier_without_firstname(self):
        login = CourierHelper.generate_random_string(10)
        password = CourierHelper.generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            # firstName отсутствует
        }

        response = CourierAPI.create_courier(payload)
        assert response.status_code == 201
        assert response.json() == {"ok": True}

        # Проверяем, что курьер создан - логинимся
        login_response = CourierAPI.login_courier({"login": login, "password": password})
        assert login_response.status_code == 200
        courier_id = login_response.json().get("id")
        
        # Удаляем курьера
        CourierAPI.delete_courier(courier_id)

    @allure.title("Успешный запрос на создание курьера возвращает {{ok:true}}")
    def test_create_courier_returns_ok(self):
        login = CourierHelper.generate_random_string(10)
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
        login, password, first_name = CourierHelper.register_new_courier_and_return_login_password()
        assert login is not None

        payload = {
            "login": login,
            "password": CourierHelper.generate_random_string(10),
            "firstName": CourierHelper.generate_random_string(10),
        }
        response = CourierAPI.create_courier(payload)

        assert response.status_code == 409
        assert response.json().get("message") == CourierData.INVALID_LOGIN_MESSAGES["duplicate_login"]

        login_response = CourierAPI.login_courier({"login": login, "password": password})
        courier_id = login_response.json().get("id")
        CourierAPI.delete_courier(courier_id)