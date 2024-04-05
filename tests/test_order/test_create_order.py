import allure
import json
from endpoints.order.create_order import CreateOrder
from endpoints.base_endpoints import BaseEndpoints
from schemas.order.create_order_schemas import PostOkSchema, PostErrorSchema


class TestLoginUser:

    @classmethod
    def setup_class(cls):
        cls.create_order = CreateOrder()
        cls.base = BaseEndpoints()

    @allure.title('Проверка создания заказа с авторизацией')
    def test_create_order_with_auth(self, login_user):
        payload = {
            "ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]
        }
        access_token = login_user["access_token"]
        response = self.create_order.post_request_with_auth(payload, access_token)
        response_status_code = self.base.check_response_status_code(response)
        response_text = self.base.check_response_text(response)
        response_schema = PostOkSchema.parse_raw(json.dumps(response_text))
        expected_result = response_schema.success
        assert response_status_code == 200 and expected_result == True, f'Статус код {response_text} не равен 200 или поле success не содержит True(фактический результат - {expected_result})'

    @allure.title('Проверка создания заказа без авторизации')
    def test_create_order_without_auth(self):
        payload = {
            "ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]
        }
        response = self.create_order.post_request_without_auth(payload)
        response_status_code = self.base.check_response_status_code(response)
        response_text = self.base.check_response_text(response)
        response_schema = PostOkSchema.parse_raw(json.dumps(response_text))
        expected_result = response_schema.success
        assert response_status_code == 200 and expected_result == True, f'Статус код {response_text} не равен 200 или поле success не содержит True(фактический результат - {expected_result})'

    @allure.title('Проверка создания заказа без ингредиентов с авторизацией')
    def test_create_order_without_ingredients_with_auth(self,login_user):
        payload = {
            "ingredients": []
        }
        access_token = login_user["access_token"]
        response = self.create_order.post_request_with_auth(payload, access_token)
        response_status_code = self.base.check_response_status_code(response)
        response_text = self.base.check_response_text(response)
        PostErrorSchema.parse_obj(response_text)
        expected_body = {
            "success": False,
            "message": "Ingredient ids must be provided"
        }
        assert response_status_code == 400 and expected_body == response_text, f'Статус код - {response_status_code} и тело ответа - {response_text}'

    @allure.title('Проверка создания заказа без ингредиентов без авторизации')
    def test_create_order_without_ingredients_without_auth(self):
        payload = {
            "ingredients": []
        }
        response = self.create_order.post_request_without_auth(payload)
        response_status_code = self.base.check_response_status_code(response)
        response_text = self.base.check_response_text(response)
        PostErrorSchema.parse_obj(response_text)
        expected_body = {
            "success": False,
            "message": "Ingredient ids must be provided"
        }
        assert response_status_code == 400 and expected_body == response_text, f'Статус код - {response_status_code} и тело ответа - {response_text}'

    @allure.title('Проверка создания заказа с неверным хешем ингредиентов')
    def test_create_order_with_incorrect_hash(self):
        payload = {
            "ingredients": ["61c0c5a71d1f8200142342", "61c0c5a71d1f8200123422"]
        }
        response = self.create_order.post_request_without_auth(payload)
        response_status_code = self.base.check_response_status_code(response)
        assert response_status_code == 500, f'Статус код - {response_status_code}'