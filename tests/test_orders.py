import allure
from faker import Faker
faker = Faker()
import requests
from constants import Constants, Constants_3


class TestOrdersUser():

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


    @allure.title('Создание заказа с авторизацией и ингридиентами')
    def test_create_order_with_auth(self):
        response = requests.post(Constants.CREATE_ORDER_URL, json=Constants_3.ORDER_DATA,
                                 headers={'Authorization': f"Bearer {self.token}"})
        assert response.status_code == 200 and response.json()['success'] == True

    @allure.title('Создание заказа без авторизации')
    def test_create_order_without_auth(self):
        response = requests.post(Constants.CREATE_ORDER_URL, json=Constants_3.ORDER_DATA)
        assert response.status_code == 200 and response.json()['success'] == True

    @allure.title('Создание заказа с ингредиентами')
    def test_create_order_without_ingredients(self):
        response = requests.post(Constants.CREATE_ORDER_URL)
        assert (response.status_code == 400 and response.json()
                == {'message': 'Ingredient ids must be provided', 'success': False})

    @allure.title('Создание заказа с неверным хешем ингредиентов')
    def test_create_order_with_invalid_ingredients(self):
        response = requests.post(Constants.CREATE_ORDER_URL, json={"ingredients": ["8946", "86706078"]})
        assert response.status_code == 500


