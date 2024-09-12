import allure
import requests
from faker import Faker
faker = Faker()
from constants import Constants



class TestEditDataUser():
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

    @allure.title('Изменить данные пользователя с авторизацией (имя)')
    def test_edit_name_with_auth(self):
        payload = {
            'email': self.user_data['email'],
            'password': self.user_data['password'],
            'name': faker.name()
        }
        response = requests.patch(Constants.EDIT_USER_URL, json=payload, headers={'Authorization': f"Bearer {self.token}"})
        assert response.status_code == 200 and response.json()['success'] == True

    @allure.title('Изменить данные пользователя с авторизацией (email)')
    def test_edit_email_with_auth(self):
        payload = {
            'email': faker.email(),
            'password': self.user_data['password'],
            'name': self.user_data['name']
        }
        response = requests.patch(Constants.EDIT_USER_URL, json=payload, headers={'Authorization': f"Bearer {self.token}"})
        assert response.status_code == 200 and response.json()['success'] == True

    @allure.title('Изменить данные пользователя с авторизацией (password)')
    def test_edit_password_with_auth(self):
        payload = {
            'email': self.user_data['email'],
            'password': faker.password(),
            'name': self.user_data['name']
        }
        response = requests.patch(Constants.EDIT_USER_URL, json=payload, headers={'Authorization': f"Bearer {self.token}"})
        assert response.status_code == 200 and response.json()['success'] == True


    @allure.title('Изменить данные пользователя без авторизации (имя)')
    def test_edit_name_without_auth(self):
        payload = {
            'email': faker.email(),
            'password': faker.password(),
            'name': faker.name()
        }
        response = requests.patch(Constants.EDIT_USER_URL, json=payload)
        assert (response.status_code == 401 and
                response.json() == {"success": False, "message": "You should be authorised"})

    @allure.title('Изменить данные пользователя без авторизации (email)')
    def test_edit_email_without_auth(self):
        payload = {
            'email': faker.email(),
            'password': self.user_data['password'],
            'name': self.user_data['name']
        }
        response = requests.patch(Constants.EDIT_USER_URL, json=payload)
        assert (response.status_code == 401 and
                response.json() == {"success": False, "message": "You should be authorised"})

    @allure.title('Изменить данные пользователя без авторизации (password)')
    def test_edit_password_without_auth(self):
        payload = {
            'email': self.user_data['email'],
            'password': faker.password(),
            'name': self.user_data['name']
        }
        response = requests.patch(Constants.EDIT_USER_URL, json=payload)
        assert (response.status_code == 401 and
                response.json() == {"success": False, "message": "You should be authorised"})

