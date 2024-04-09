import requests
import allure
from data import URL_AUTH


class CreateNewUser:

    @allure.step('Создаём нового пользователя')
    def post_request(self, payload):
        return requests.post(
            f'{URL_AUTH}/register', data=payload, timeout=10)
