import requests
import random
import string
import json 

base = "http://127.0.0.1:8000/" 

create_url = "create_user/"
get_url = "users/"

def get_user_url(user_email: str) -> str:
    return base + get_url + user_email

def create_user_data(name: str, email: str, password: str) -> dict:
    return {
        "name": name,
        "email": email,
        "password": password
    }

def generate_random_string(length: int = 8) -> str:
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def generate_random_users(n: int) -> list:
    users = []
    for i in range(n):
        name = generate_random_string()
        email = generate_random_string() + "@gmail.com"
        password = generate_random_string()
        users.append(create_user_data(name, email, password))
    return users

def post_create_users():
    users = generate_random_users(1)
    for user in users:
        print(json.dumps(user))
        response = requests.post(base + create_url, json=user)
        print(response.ok)        
        print(response.json())        


def main():
    print("running main")
    post_create_users()


if __name__ == "__main__":
    main()
