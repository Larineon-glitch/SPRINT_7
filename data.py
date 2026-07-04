class CourierData:
    DEFAULT_PASSWORD = "password123"
    DEFAULT_FIRST_NAME = "John"

    INVALID_LOGIN_MESSAGES = {
        "missing_login": "Недостаточно данных для создания учетной записи",
        "missing_password": "Недостаточно данных для создания учетной записи",
        "duplicate_login": "Этот логин уже используется. Попробуйте другой.",
    }

    LOGIN_ERROR_MESSAGES = {
        "missing_field": "Недостаточно данных для входа",
        "invalid_credentials": "Учетная запись не найдена",
    }


class OrderData:
    DEFAULT_COLORS = ["BLACK"]
    STATION_FROM = 4
    STATION_TO = 5


    
    ORDER_FIELDS = {
        "firstName": "Балерина",
        "lastName": "Капучино",
        "address": "ул. Новый Арбат, 20",
        "metroStation": 4,
        #"metro_station": "Чистые пруды",        
        "phone": "+79123456789",
        "rentTime": 3,
        "deliveryDate": "2026-07-10",
        #"delivery_date": "10.08.2026",        
        "comment": "Позвонить за 3 часа",
            #"delivery_date": "10.08.2026",
            #"rental_period": "двое суток",
            #"color": ["чёрный жемчуг"], 
    }

    # Варианты цветов для параметризации
    COLOR_VARIANTS = [
        (["BLACK"], "black"),
        (["GREY"], "grey"),
        (["BLACK", "GREY"], "both"),
        ([], "none"),
    ]
