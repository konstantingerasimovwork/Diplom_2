import allure
import json
from endpoints.user.login_user import LoginUser
from endpoints.base_endpoints import BaseEndpoints
from schemas.user.login_user_schemas import PostOkSchema, PostErrorSchema, UserData


class TestLoginUser:

    @classmethod
    def setup_class(cls):
        cls.login_user = LoginUser()
        cls.base = BaseEndpoints()

    @allure.title('Проверка авторизации под существующим пользователем')
    def test_login_existing_user(self, registration):
        payload = {
            "email": registration['email'],
            "password": registration['password']
        }
        access_token = registration['access_token']
        response = self.login_user.post_request(payload, access_token)
        response_status_code = self.base.check_response_status_code(response)
        response_text = self.base.check_response_text(response)
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
                "email": registration['email'],
                "name": registration['name']
            }
        }
        assert response_status_code == 200 and response_text == expected_body, f'Статус код - {response_status_code} и тело ответа - {response_text}'
    
    @allure.title('Проверка авторизации пользователя с неправильным email')
    def test_login_with_incorrect_email(self, registration):
        payload = {
            "email": 'test@test.com',
            "password": registration['password']
        }
        access_token = registration['access_token']
        response = self.login_user.post_request(payload, access_token)
        response_status_code = self.base.check_response_status_code(response)
        response_text = self.base.check_response_text(response)
        PostErrorSchema.parse_obj(response_text)
        expected_body = {
            "success": False,
            "message": "email or password are incorrect"
        }
        assert response_status_code == 401 and response_text == expected_body, f'Статус код - {response_status_code} и тело ответа - {response_text}'

    @allure.title('Проверка авторизации пользователя с неправильным password')
    def test_login_with_incorrect_password(self, registration):
        payload = {
            "email": registration['email'],
            "password": 'test_password'
        }
        access_token = registration['access_token']
        response = self.login_user.post_request(payload, access_token)
        response_status_code = self.base.check_response_status_code(response)
        response_text = self.base.check_response_text(response)
        PostErrorSchema.parse_obj(response_text)
        expected_body = {
            "success": False,
            "message": "email or password are incorrect"
        }
        assert response_status_code == 401 and response_text == expected_body, f'Статус код - {response_status_code} и тело ответа - {response_text}'
