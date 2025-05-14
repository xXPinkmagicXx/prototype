import grpc
from . import user_pb2
from . import user_pb2_grpc
import string
import random
import time
from . import utils

def create_user(stub, username, email):
  """Creates a user using the gRPC stub."""
  user = user_pb2.User(username=username, email=email)
  response = stub.CreateUser(user)
  return response



def post_create_user_insecure(username) -> str:
  """Runs the client application."""
  # Replace 'localhost:50051' with your server address.
  with grpc.insecure_channel('localhost:50051') as channel:
      stub = user_pb2_grpc.UserServiceStub(channel)

      email = username + "@gmail.com"

      response = create_user(stub, username, email)
      return response.success
    
   
def post_create_user_secure_2(username: str) -> bool:
   email = username + "@gmail.com"
   utils.create_secure_stub_and_run(lambda stub: create_user(stub, username, email))

def post_create_user_secure(username: str)-> bool:
  """Runs the client application."""
  # Replace 'localhost:50051' with your server address.
  with open('server.crt', 'rb') as f:
    trusted_certs = f.read()

  credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
  with grpc.secure_channel('localhost:50051', credentials=credentials) as channel:
    stub = user_pb2_grpc.UserServiceStub(channel)

    email = username + "@gmail.com"
    response = create_user(stub, username, email)

    return response.success

def generate_random_users(n: int) -> list:
    users: list[str] = []
    for i in range(n):
        name = generate_random_string()
        users.append(name)
    return users

def generate_random_string(length: int = 8) -> str:
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def run_create_user_experiment_insecure(n_requests: int) -> tuple[float, float, list]:
   users = generate_random_users(n_requests)    
   begin_time = time.time()
   for user in users :
      success = post_create_user_insecure(user)
   timer_after = time.time()
   total_time = timer_after - begin_time
   
   # Calculate metrics
   avg_time_per_request = total_time / n_requests
   request_per_second = n_requests / total_time   

   avg_time_per_request_ms = avg_time_per_request * 1000
   return avg_time_per_request_ms, request_per_second, users

def run_create_user_experiment_secure(n_requests: int) -> tuple[float, float, list]:
   """Runs the client application."""
   # Replace 'localhost:50051' with your server address.
   usernames = generate_random_users(n_requests)    
   begin_time = time.time()
   for user in usernames:
      success = post_create_user_secure_2(user)
   timer_after = time.time()
   total_time = timer_after - begin_time
   
   # Calculate metrics
   avg_time_per_request = total_time / n_requests
   request_per_second = n_requests / total_time   
   
   avg_time_per_request_ms = avg_time_per_request * 1000
   return avg_time_per_request_ms, request_per_second, usernames

if __name__ == '__main__':
    
  n_requests = 10_000
  avg_time_per_request, request_per_second = run_create_user_experiment_insecure(n_requests)

  print("Request per second: ", request_per_second)
  print("avg time per reqest: ", avg_time_per_request*1000, "ms")
