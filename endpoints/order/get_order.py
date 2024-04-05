import requests
import allure
from data import URL_ORDER


class GetOrder:

    @allure.step('Получение заказа без авторизации')
    def get_request_without_auth(self):
        return requests.get(f'{URL_ORDER}', timeout=10)

    @allure.step('Получение заказа с авторизацией')
    def get_request_with_auth(self, access_token):
        return requests.get(
            f'{URL_ORDER}', timeout=10, headers={'Authorization': access_token})
