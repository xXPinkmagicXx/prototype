import grpc
from . import user_pb2
from . import user_pb2_grpc
import string
import random
import time

def create_user(stub, username, email):
  """Creates a user using the gRPC stub."""
  user = user_pb2.User(username=username, email=email)
  response = stub.CreateUser(user)
  return response



def post_create_user_insecure():
  """Runs the client application."""
  # Replace 'localhost:50051' with your server address.
  with grpc.insecure_channel('localhost:50051') as channel:
    stub = user_pb2_grpc.UserServiceStub(channel)

    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 8))
    username = "user" + random_string
    email = username + "@gmail.com"

    response = create_user(stub, username, email)

    if response.success:
      #print(f"User created successfully! User ID: {response.user_id}")
      return
    else:
      print(f"Failed to create user. Error: {response.error_message}")
def post_create_user_secure():
  """Runs the client application."""
  # Replace 'localhost:50051' with your server address.
  with open('server.crt', 'rb') as f:
    trusted_certs = f.read()

  credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
  with grpc.secure_channel('localhost:50051', credentials=credentials) as channel:
    stub = user_pb2_grpc.UserServiceStub(channel)

    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 8))
    username = "user" + random_string
    email = username + "@gmail.com"

    response = create_user(stub, username, email)

    if response.success:
      #print(f"User created successfully! User ID: {response.user_id}")
      return
    else:
      print(f"Failed to create user. Error: {response.error_message}")
  

def run_create_user_experiment(n_requests: int) -> tuple[float, float]:
    
   begin_time = time.time()
   for _ in range(n_requests):
      post_create_user_insecure()
   timer_after = time.time()
   total_time = timer_after - begin_time
   
   # Calculate metrics
   avg_time_per_request = total_time / n_requests
   request_per_second = n_requests / total_time   

   avg_time_per_request_ms = avg_time_per_request * 1000
   return avg_time_per_request_ms, request_per_second

def run_create_user_experiment_secure(n_requests: int) -> tuple[float, float]:
   """Runs the client application."""
   # Replace 'localhost:50051' with your server address.

   begin_time = time.time()
   for _ in range(n_requests):
      post_create_user_secure()
   timer_after = time.time()
   total_time = timer_after - begin_time
   
   # Calculate metrics
   avg_time_per_request = total_time / n_requests
   request_per_second = n_requests / total_time   
   
   avg_time_per_request_ms = avg_time_per_request * 1000
   return avg_time_per_request_ms, request_per_second

if __name__ == '__main__':
    
  n_requests = 10_000
  avg_time_per_request, request_per_second = run_create_user_experiment(n_requests)

  print("Request per second: ", request_per_second)
  print("avg time per reqest: ", avg_time_per_request*1000, "ms")
