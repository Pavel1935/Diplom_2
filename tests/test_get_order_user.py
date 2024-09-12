import allure
import requests
from faker import Faker
faker = Faker()
from constants import Constants

class TestGetOrderUser():
    @classmethod
    def setup_class(cls):
        cls.user_data = {
            'email': faker.email(),
            'password': faker.password(),
            'name': faker.name()
        }

        response = requests.post(Constants.CREATE_USER_URL, json=cls.user_data)
        cls.token = response.json()['accessToken'].replace('Bearer ', '')

    @classmethod
    def teardown_class(cls):
        requests.delete(Constants.DELETE_USER_URL, headers={'Authorization': cls.token})


    @allure.title('Получение заказов авторизованного пользователя')
    def test_get_order_auth_user(self):
        response = requests.get(Constants.GET_ORDER_URL, headers={'Authorization': f"Bearer {self.token}"})
        assert response.status_code == 200 and response.json()['success'] == True

    @allure.title('Получение заказов неавторизованного пользователя')
    def test_get_order_with_auth_user(self):
        response = requests.get(Constants.GET_ORDER_URL, headers=None)
        assert response.status_code == 401 and {"success": 'false', "message": "You should be authorised"}
