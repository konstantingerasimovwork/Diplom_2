import allure
import json
from endpoints.user.change_data_user import ChangeDataUser
from endpoints.base_endpoints import BaseEndpoints
from schemas.user.change_data_user_schemas import PostOkSchema, PostErrorSchema, UserData
from helpers import user_data
from response_data import NON_AUTHORIZED

class TestChangeData:

    @classmethod
    def setup_class(cls):
        cls.change_data_user = ChangeDataUser()
        cls.base = BaseEndpoints()

    @allure.title('Проверка изменения email пользователя с авторизацией')
    def test_change_user_email_after_auth(self, login_user):
        data = user_data()
        params = {'email': data['email']}
        access_token = login_user['access_token']
        response = self.change_data_user.patch_request_with_auth(params, access_token)
        response_status_code = self.base.check_response_status_code(response)
        response_text = self.base.check_response_text(response)
        PostOkSchema.parse_obj(response_text)
        response_schema = PostOkSchema.parse_raw(json.dumps(response_text))
        UserData.parse_obj(response_schema.user)
        expected_result = {
            "success": True,
            "user": {
                "email": data['email'],
                "name": login_user['name']
            }
        }
        assert response_status_code == 200 and expected_result == response_text, f'Статус код - {response_status_code} и тело ответа - {response_text}'

    @allure.title('Проверка изменения name пользователя с авторизацией')
    def test_change_user_name_after_auth(self, login_user):
        data = user_data()
        params = {'name': data['name']}
        access_token = login_user['access_token']
        response = self.change_data_user.patch_request_with_auth(
            params, access_token)
        response_status_code = self.base.check_response_status_code(response)
        response_text = self.base.check_response_text(response)
        PostOkSchema.parse_obj(response_text)
        response_schema = PostOkSchema.parse_raw(json.dumps(response_text))
        UserData.parse_obj(response_schema.user)
        expected_result = {
            "success": True,
            "user": {
                "email": login_user['email'],
                "name": data['name']
            }
        }
        assert response_status_code == 200 and expected_result == response_text, f'Статус код - {response_status_code} и тело ответа - {response_text}'

    @allure.title('Проверка изменения email пользователя без авторизации')
    def test_change_user_email_without_auth(self):
        data = user_data()
        params = {'email': data['email']}
        response = self.change_data_user.patch_request_without_auth(params)
        response_status_code = self.base.check_response_status_code(response)
        response_text = self.base.check_response_text(response)
        PostErrorSchema.parse_obj(response_text)
        expected_result = NON_AUTHORIZED
        assert response_status_code == 401 and expected_result == response_text, f'Статус код - {response_status_code} и тело ответа - {response_text}'

    @allure.title('Проверка изменения name пользователя без авторизации')
    def test_change_user_name_without_auth(self):
        data = user_data()
        params = {'name': data['name']}
        response = self.change_data_user.patch_request_without_auth(params)
        response_status_code = self.base.check_response_status_code(response)
        response_text = self.base.check_response_text(response)
        PostErrorSchema.parse_obj(response_text)
        expected_result = NON_AUTHORIZED
        assert response_status_code == 401 and expected_result == response_text, f'Статус код - {response_status_code} и тело ответа - {response_text}'
