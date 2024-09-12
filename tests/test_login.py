import allure
import requests
from faker import Faker
faker = Faker()
from constants import Constants



class TestLoginUser():
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


    @allure.title('Логин под существующим пользователем')
    def test_login_OK(self):
        payload = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = requests.post(Constants.LOGIN_USER_URL, json=payload)
        assert response.status_code == 200 and response.json()['success'] == True


    @allure.title('Логин под несуществующим пользователем')
    def test_login_invalid_username_password(self):
        payload = {
            'email': self.user_data['email'],
            'password': 'wrong_password'
        }
        response = requests.post(Constants.LOGIN_USER_URL, json=payload)
        assert response.status_code == 401 and {"success": 'false',
    "message": "email or password are incorrect"}


    @allure.title('Удаление пользователя')
    def test_delete_user(self):
        payload = self.user_data
        response = requests.delete(Constants.DELETE_USER_URL, json=payload,
                                   headers={'Authorization': f"Bearer {self.token}"})
        assert response.status_code == 202 and {"success": 'true', "message": "User successfully removed"}


