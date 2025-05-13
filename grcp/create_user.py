import grpc
import user_pb2
import user_pb2_grpc
import string
import random
import time

def create_user(stub, username, email):
  """Creates a user using the gRPC stub."""
  user = user_pb2.User(username=username, email=email)
  response = stub.CreateUser(user)
  return response

def run():
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

def run_create_user_experiment(n_requests: int) -> tuple[float, float]:
    
    begin_time = time.time()
    for _ in range(n_requests):
        run()
    timer_after = time.time()
    total_time = timer_after - begin_time
    
    # Calculate metrics
    avg_time_per_request = total_time / n_requests
    request_per_second = n_requests / total_time   

    return request_per_second, avg_time_per_request

if __name__ == '__main__':
    
  n_requests = 10_000
  request_per_second, avg_time_per_request = run_create_user_experiment(n_requests)

  print("Request per second: ", request_per_second)
  print("avg time per reqest: ", avg_time_per_request*1000, "ms")
