import allure


class BaseEndpoints:

    @allure.step('Получаем содержимое ответа')
    def check_response_text(self, response):
        return response.json()

    @allure.step('Получаем статус код')
    def check_response_status_code(self, response):
        return response.status_code
