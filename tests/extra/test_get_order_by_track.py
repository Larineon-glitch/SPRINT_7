import allure

from api.order_api import OrderAPI


@allure.feature("Получение заказа по его номеру (дополнительное задание)")
class TestGetOrderByTrack:

    @allure.title("Успешный запрос возвращает объект с заказом")
    def test_get_order_by_track_success(self, create_order_and_return_track):
        track = create_order_and_return_track
        if not track:
            allure.skip("Заказ не был создан")

        params = {"t": track}
        response = OrderAPI.get_order_by_track(params=params)

        assert response.status_code == 200
        assert "order" in response.json()
        order = response.json()["order"]
        assert "id" in order
        assert "track" in order
        assert order["track"] == track

    @allure.title("Запрос без номера заказа возвращает ошибку")
    def test_get_order_by_track_without_track(self):
        response = OrderAPI.get_order_by_track(params={})
        assert response.status_code == 400
        assert "Недостаточно данных для поиска" in response.text

    @allure.title("Запрос с несуществующим заказом возвращает ошибку")
    def test_get_order_by_track_nonexistent(self):
        params = {"t": 999999}
        response = OrderAPI.get_order_by_track(params=params)
        assert response.status_code == 404
        assert "Заказ не найден" in response.text