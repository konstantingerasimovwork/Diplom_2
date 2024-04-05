import requests
import allure
from data import URL_ORDER


class CreateOrder:

    @allure.step('Создание заказа без авторизации')
    def post_request_without_auth(self, payload):
        return requests.post(f'{URL_ORDER}', data=payload, timeout=10)
    
    @allure.step('Создание заказа с авторизацией')
    def post_request_with_auth(self, payload, access_token):
        return requests.post(
            f'{URL_ORDER}', data=payload, timeout=10, headers={'Authorization': access_token})
