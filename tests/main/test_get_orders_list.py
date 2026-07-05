import allure

from api.order_api import OrderAPI


@allure.feature("Список заказов")
class TestGetOrdersList:

    @allure.title("В тело ответа возвращается список заказов")
    def test_get_orders_list_returns_list(self):
        response = OrderAPI.get_orders_list()

        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)

    @allure.title("Список заказов можно получить с параметрами")
    def test_get_orders_list_with_params(self):
        params = {"limit": 5}
        response = OrderAPI.get_orders_list(params=params)

        assert response.status_code == 200
        assert "orders" in response.json()
        assert len(response.json()["orders"]) <= 5