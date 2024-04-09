import requests
import allure
from data import URL_AUTH


class ChangeDataUser:

    @allure.step('Изменяем данные пользователя с авторизацией')
    def patch_request_with_auth(self, params, access_token):
        return requests.patch(
            f'{URL_AUTH}/user', data=params, timeout=10, headers={'Authorization': access_token})

    @allure.step('Изменяем данные пользователя без авторизации')
    def patch_request_without_auth(self, params):
        return requests.patch(
            f'{URL_AUTH}/user', data=params, timeout=10)
