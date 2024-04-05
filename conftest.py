import pytest
import requests
import json
from data import URL_AUTH, URL_ORDER
from helpers import user_data
from schemas.user.create_new_user_schemas import PostOkSchema


@pytest.fixture(scope="function")
def registration():

    data = user_data()
    payload = {
        "email": data['email'],
        "password": data['password'],
        "name": data['name']
    }
    user_login_data = {}
    response = requests.post(f'{URL_AUTH}/register', data=payload, timeout=10)
    response_text = response.json()
    response_schema = PostOkSchema.parse_raw(json.dumps(response_text))
    access_token = response_schema.accessToken

    if response.status_code == 200:
        user_login_data["email"] = data['email']
        user_login_data["password"] = data['password']
        user_login_data["name"] = data['name']
        user_login_data["access_token"] = access_token
    yield user_login_data
    response = requests.delete(f'{URL_AUTH}/user', timeout=10,
                               headers={'Authorization': user_login_data["access_token"]})
    assert response.status_code == 202, response.json()


@pytest.fixture(scope="function")
def login_user(registration):

    payload = {
        "email": registration['email'],
        "password": registration['password']
    }
    response = requests.post(f'{URL_AUTH}/login', data=payload, timeout=10, headers={'Autorization': registration['access_token']})
    response_text = response.json()
    response_schema = PostOkSchema.parse_raw(json.dumps(response_text))
    access_token = response_schema.accessToken
    user_login_data = {}
    if response.status_code == 200:
        user_login_data["email"] = registration['email']
        user_login_data["name"] = registration['name']
        user_login_data["access_token"] = access_token
    yield user_login_data

@pytest.fixture(scope="function")
def create_order(login_user):
    payload = {
        "ingredients": ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]
    }
    access_token = login_user["access_token"]
    response = requests.post(f'{URL_ORDER}', data=payload, timeout=10, headers={'Autorization': access_token})
    if response.status_code == 200:
        yield access_token