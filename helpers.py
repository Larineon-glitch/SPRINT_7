import random
import string
import time

from api.courier_api import CourierAPI


class CourierHelper:
    @staticmethod
    def generate_random_string(length=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    @staticmethod
    def register_new_courier_and_return_login_password(max_retries=5):
        # Регистрирует нового курьера с повторными попытками при конфликте логина
         
        for attempt in range(max_retries):
            timestamp = str(int(time.time() * 1000))[-8:]
            random_part = CourierHelper.generate_random_string(8)
            login = f"{random_part}_{timestamp}_{attempt}"
            password = CourierHelper.generate_random_string(10)
            first_name = CourierHelper.generate_random_string(10)

            payload = {
                "login": login,
                "password": password,
                "firstName": first_name,
            }

            response = CourierAPI.create_courier(payload)

            if response.status_code == 201:
                print(f"Курьер создан с логином: {login}")  
                return login, password, first_name
            elif response.status_code == 409:
                print(f"Логин {login} уже существует, пробуем снова...")
                continue
            else:
                print(f"Ошибка при создании курьера: {response.status_code} - {response.text}")
                break
        
        print("Не удалось создать курьера после всех попыток")
        return None, None, None

    @staticmethod
    def create_and_login_courier():
        login, password, first_name = CourierHelper.register_new_courier_and_return_login_password()
        if login and password:
            login_payload = {"login": login, "password": password}
            response = CourierAPI.login_courier(login_payload)
            if response.status_code == 200:
                courier_id = response.json().get("id")
                return login, password, first_name, courier_id
        return None, None, None, None