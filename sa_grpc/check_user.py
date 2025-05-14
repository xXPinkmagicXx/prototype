import grpc
from . import user_pb2
from . import user_pb2_grpc
import string
import random
import time
import sys
from . import run_create_user_experiment_insecure, run_create_user_experiment_secure


def check_user(stub, username):
  """Checks user using the gRPC stub."""
  user = user_pb2.User(username=username)
  response = stub.CheckUser(user)
  return response


def run_get_user_experiment_insecure(n_requests:int, users_created: bool) -> tuple[float, float]:
   # Create
   if not users_created:
      _, _, usernames = run_create_user_experiment_insecure(n_requests)

   begin_time = time.time()
   for username in usernames:
      user = get_user(username)
   timer_after = time.time()
   total_time = timer_after - begin_time
   
   avg_response_time = total_time/n_requests
   avg_response_time_ms = avg_response_time * 1000
   
   request_per_second = n_requests / total_time
   
   return avg_response_time_ms, request_per_second

def get_user(username: str):
  """Runs the client application."""
  # Replace 'localhost:50051' with your server address.
  with grpc.insecure_channel('localhost:50051') as channel:
    
      stub = user_pb2_grpc.UserServiceStub(channel)
      response = check_user(stub, username)

      if response.success:
         return response.user_id

def main():
  
  begin_time = time.time()
  n_requests = 10000
  
  for i in range(n_requests):
      get_user()
  
  timer_after = time.time()
  total_time = timer_after - begin_time
  avg_time_per_request = total_time/n_requests

  request_per_second = n_requests / total_time
  
  print("Request per second: ", request_per_second)
  print("avg time per reqest: ", avg_time_per_request*1000, "ms")

if __name__ == '__main__':
   main()


