import allure
import json
from endpoints.order.get_order import GetOrder
from endpoints.base_endpoints import BaseEndpoints
from schemas.order.get_order_schemas import PostOkSchema, PostErrorSchema


class TestGetOrder:

    @classmethod
    def setup_class(cls):
        cls.get_order = GetOrder()
        cls.base = BaseEndpoints()

    @allure.title('Проверка получение заказов конкретного пользователя авторизованным пользователем')
    def test_get_order_with_auth(self, create_order):
        access_token = create_order
        response = self.get_order.get_request_with_auth(access_token)
        response_status_code = self.base.check_response_status_code(response)
        response_text = self.base.check_response_text(response)
        response_schema = PostOkSchema.parse_raw(json.dumps(response_text))
        expected_result = response_schema.success
        assert response_status_code == 200 and expected_result == True, f'Статус код {response_text} не равен 200 или поле success не содержит True(фактический результат - {expected_result})'

    @allure.title('Проверка получение заказов конкретного пользователя не авторизованным пользователем')
    def test_get_order_without_auth(self):
        response = self.get_order.get_request_without_auth()
        response_status_code = self.base.check_response_status_code(response)
        response_text = self.base.check_response_text(response)
        PostErrorSchema.parse_obj(response_text)
        expected_body = {
            "success": False,
            "message": "You should be authorised"
        }
        assert response_status_code == 401 and response_text == expected_body, f'Статус код - {response_status_code} и тело ответа - {response_text}'
