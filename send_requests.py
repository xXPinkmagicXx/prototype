import requests
import random
import string
import json 
import time
import constants as c

base = "http://127.0.0.1:8000/" 
create_url = "create_user/"
get_url = "users/"

user_emails: list[str] = [] 

def get_user_url(user_email) -> str:
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
        user_emails.append(email)
        password = generate_random_string()
        users.append(create_user_data(name, email, password))
    return users

def post_create_users(n_users: int = 1000)-> tuple[float, float]:
   users = generate_random_users(n_users)
   response_times_sum = 0
   begin_time = time.time()
   for user in users:
      time_before = time.time()
      response = requests.post(base + create_url, json=user)
      time_after = time.time()
      response_times_sum += time_after - time_before
   end_time = time.time()
   
   total_time = end_time - begin_time
   avg_response_time = response_times_sum / n_users
   avg_response_time_ms = avg_response_time * 1000
   
   return (avg_response_time_ms, n_users / total_time)

def post_create_users_secure(n_users: int) -> tuple[float, float]:
   users = generate_random_users(n_users)
   response_times_sum = 0
   begin_time = time.time()
   for user in users:
      time_before = time.time()
      response = requests.post(c.BASE_SECURE_URL + create_url, json=user, cert=(c.SERVER_CERTIFICATE_PATH, c.SERVER_PRIVATE_KEY_PATH), verify=False)
      time_after = time.time()
      response_times_sum += time_after - time_before
   end_time = time.time()
   
   total_time = end_time - begin_time
   avg_response_time = response_times_sum / n_users
   avg_response_time_ms = avg_response_time * 1000
   
   return (avg_response_time_ms, n_users / total_time)


def get_user(url: str, args: list)-> requests.Response:
    response = requests.get(url, json=args[0])
    return response

def get_users(n_users: int = 1000, users_created = True)-> tuple[float, float]:
    if not users_created:
        post_create_users(n_users)
    
    begin_time = time.time()
    response_times_sum = 0
    for user_email in user_emails: # user_emails global variable
        time_before = time.time()
        response = requests.get(get_user_url(user_email))
        time_after = time.time()
        response_times_sum += time_after - time_before
    end_time = time.time()

    total_time = end_time - begin_time
    request_per_sec = n_users / total_time
    avg_response_time = response_times_sum / n_users
    avg_response_time_ms = avg_response_time * 1000

    return (avg_response_time_ms, request_per_sec)

def get_users_secure(n_users: int, users_created = True) -> tuple[float, float]:
    if not users_created:
        post_create_users_secure(n_users)
    
    begin_time = time.time()
    response_times_sum = 0
    for user_email in user_emails:
        time_before = time.time()
        response = requests.get(c.REST_SECURE_GET_URL + user_email, verify=False)
        time_after = time.time()
        response_times_sum += time_after - time_before
    end_time = time.time()

    total_time = end_time - begin_time
    request_per_sec = n_users / total_time
    avg_response_time = response_times_sum / n_users
    avg_response_time_ms = avg_response_time * 1000

    return (avg_response_time_ms, request_per_sec)

def main():
    print("running main")
    
    n_users = 5000
    print(f"Now creating {n_users} users.")
    avg_response_time_create_users, requests_pr_sec_create_users = post_create_users(n_users)
    
    print(f"Now getting {n_users} users.")
    avg_response_time_get_users, requests_pr_sec_get_users = get_users(n_users, users_created=True)

    print("Create users: avg response time (ms): ", avg_response_time_create_users, "; requests per second: ", requests_pr_sec_create_users)
    print("Get users: avg response time (ms):  ", avg_response_time_get_users, "; requests per second: ", requests_pr_sec_get_users)

if __name__ == "__main__":
    main()
