import requests
import allure
from data import URL_AUTH


class LoginUser:

    @allure.step('Логин пользователя')
    def post_request(self, payload, access_token):
        return requests.post(
            f'{URL_AUTH}/login', data=payload, timeout=10, headers={'Authorization': access_token})
