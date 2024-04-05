from faker import Faker

def user_data():
    fake = Faker()
    return {
        'email': fake.email(),
        'password': fake.password(),
        'name': fake.name()
    }