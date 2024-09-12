import allure
import requests
from faker import Faker
faker = Faker()
from constants import Constants

class TestCreateUser():

    @classmethod
    def setup_class(cls):
        cls.user_data = {'email': faker.email(),
                        'password': faker.password(),
                        'name': faker.name()
                         }

    @classmethod
    def teardown_class(cls):
        login_payload = {
                'email': cls.user_data['email'], 'password': cls.user_data['password']
             }
        login_response = requests.post(Constants.LOGIN_USER_URL, json=login_payload)
        token = login_response.json().get('accessToken')
        headers = {
            'Authorization': token}
        requests.delete(Constants.DELETE_USER_URL, headers=headers)

    @allure.title('создать уникального пользователя')
    def test_create_user_OK(self):
        payload = self.user_data
        response = requests.post(Constants.CREATE_USER_URL, json=payload)
        assert response.status_code == 200 and response.json()['success'] == True

    @allure.title('создать пользователя, который уже зарегистрирован')
    def test_create_registered_user_fail(self):
        payload = self.user_data
        response = requests.post(Constants.CREATE_USER_URL, json=payload)
        assert (response.status_code == 403 and response.json()
                == {'message': 'User already exists', 'success': False})

    @allure.title('создать пользователя и не заполнить одно из обязательных полей')
    def test_without_login_error(self):
        payload = {
                'email': '',
                'password': faker.password(),
                'name': faker.name()
        }
        response = requests.post(Constants.CREATE_USER_URL, json=payload)
        assert (response.status_code == 403 and response.json()
                == {'message': 'Email, password and name are required fields', 'success': False})
