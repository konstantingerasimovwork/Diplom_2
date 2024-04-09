import allure
import json
from endpoints.user.create_new_user import CreateNewUser
from endpoints.base_endpoints import BaseEndpoints
from schemas.user.create_new_user_schemas import PostOkSchema, PostErrorSchema, UserData
from helpers import user_data
from response_data import REQUIRED_FIELDS, USER_ALREADY_EXIST


class TestCreateUser:

    @classmethod
    def setup_class(cls):
        cls.new_user = CreateNewUser()
        cls.base = BaseEndpoints()

    @allure.title('Проверка создания уникального пользователя')
    def test_create_new_user(self):
        data = user_data()
        payload = {
            "email": data['email'],
            "password": data['password'],
            "name": data['name']
        }
        response = self.new_user.post_request(payload)
        response_text = self.base.check_response_text(response)
        response_status_code = self.base.check_response_status_code(response)
        PostOkSchema.parse_obj(response_text)
        response_schema = PostOkSchema.parse_raw(json.dumps(response_text))
        UserData.parse_obj(response_schema.user)
        access_token = response_schema.accessToken
        refreshToken = response_schema.refreshToken
        expected_body = {
            "success": True,
            "accessToken": access_token,
            "refreshToken": refreshToken,
            "user": {
                "email": data['email'],
                "name": data['name']
            }
        }
        assert response_status_code == 200 and response_text == expected_body, f'Статус код - {response_status_code} и тело ответа - {response_text}'

    @allure.title('Проверка создания пользователя, который уже зарегистрирован')
    def test_create_existing_user(self, registration):
        payload = {
            "email": registration["email"],
            "password": registration["password"],
            "name": registration["name"]
        }
        response = self.new_user.post_request(payload)
        response_text = self.base.check_response_text(response)
        response_status_code = self.base.check_response_status_code(response)
        PostErrorSchema.parse_obj(response_text)
        expected_body = USER_ALREADY_EXIST
        assert response_status_code == 403 and response_text == expected_body, f'Статус код - {response_status_code} и тело ответа - {response_text}'

    @allure.title('Проверка создания нового пользователя без обязательного поля email')
    def test_create_user_without_email(self):
        data = user_data()
        payload = {
            "password": data['password'],
            "name": data['name']
        }
        response = self.new_user.post_request(payload)
        response_text = self.base.check_response_text(response)
        response_status_code = self.base.check_response_status_code(response)
        PostErrorSchema.parse_obj(response_text)
        expected_body = REQUIRED_FIELDS
        assert response_status_code == 403 and response_text == expected_body, f'Статус код - {response_status_code} и тело ответа - {response_text}'

    @allure.title('Проверка создания нового пользователя без обязательного поля password')
    def test_create_user_without_password(self):
        data = user_data()
        payload = {
            "email": data['email'],
            "name": data['name']
        }
        response = self.new_user.post_request(payload)
        response_text = self.base.check_response_text(response)
        response_status_code = self.base.check_response_status_code(response)
        PostErrorSchema.parse_obj(response_text)
        expected_body = REQUIRED_FIELDS
        assert response_status_code == 403 and response_text == expected_body, f'Статус код - {response_status_code} и тело ответа - {response_text}'

    @allure.title('Проверка создания нового пользователя без обязательного поля name')
    def test_create_user_without_name(self):
        data = user_data()
        payload = {
            "email": data['email'],
            "password": data['password']
        }
        response = self.new_user.post_request(payload)
        response_text = self.base.check_response_text(response)
        response_status_code = self.base.check_response_status_code(response)
        PostErrorSchema.parse_obj(response_text)
        expected_body = REQUIRED_FIELDS
        assert response_status_code == 403 and response_text == expected_body, f'Статус код - {response_status_code} и тело ответа - {response_text}'
