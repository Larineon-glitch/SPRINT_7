import allure
import pytest

from api.courier_api import CourierAPI
from data import CourierData
from helpers import CourierHelper


@allure.feature("Логин курьера")
class TestLoginCourier:

    @allure.title("Курьер может авторизоваться")
    def test_login_courier_success(self):
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

        login_payload = {"login": login, "password": password}
        response = CourierAPI.login_courier(login_payload)

        assert response.status_code == 200
        assert "id" in response.json()

        courier_id = response.json()["id"]
        CourierAPI.delete_courier(courier_id)

    @allure.title("Для авторизации нужно передать все обязательные поля")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_courier_missing_field(self, missing_field):
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

        login_payload = {
            "login": login,
            "password": password,
        }
        del login_payload[missing_field]

        response = CourierAPI.login_courier(login_payload)
        assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
        assert response.json().get("message") == CourierData.LOGIN_ERROR_MESSAGES["missing_field"]

        login_response = CourierAPI.login_courier({"login": login, "password": password})
        courier_id = login_response.json().get("id")
        CourierAPI.delete_courier(courier_id)

    @allure.title("Система возвращает ошибку при неправильном логине или пароле")
    @pytest.mark.parametrize("wrong_field", ["login", "password"])
    def test_login_courier_wrong_credentials(self, wrong_field):
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

        login_payload = {
            "login": login,
            "password": password,
        }
        if wrong_field == "login":
            login_payload["login"] = "wrong_login"
        else:
            login_payload["password"] = "wrong_password"

        response = CourierAPI.login_courier(login_payload)
        assert response.status_code == 404
        assert response.json().get("message") == CourierData.LOGIN_ERROR_MESSAGES["invalid_credentials"]

        login_response = CourierAPI.login_courier({"login": login, "password": password})
        courier_id = login_response.json().get("id")
        CourierAPI.delete_courier(courier_id)

    @allure.title("Авторизация под несуществующим пользователем возвращает ошибку")
    def test_login_courier_nonexistent(self):
        login_payload = {
            "login": CourierHelper.generate_unique_login(),
            "password": CourierHelper.generate_random_string(10),
        }

        response = CourierAPI.login_courier(login_payload)
        assert response.status_code == 404
        assert response.json().get("message") == CourierData.LOGIN_ERROR_MESSAGES["invalid_credentials"]

    @allure.title("Успешный запрос возвращает id курьера")
    def test_login_courier_returns_id(self):
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

        login_payload = {"login": login, "password": password}
        response = CourierAPI.login_courier(login_payload)

        assert response.status_code == 200
        assert isinstance(response.json().get("id"), int)

        courier_id = response.json()["id"]
        CourierAPI.delete_courier(courier_id)