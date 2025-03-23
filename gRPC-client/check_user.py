import grpc
import user_pb2
import user_pb2_grpc
import string
import random
import time
import sys

def check_user(stub, username):
  """Checks user using the gRPC stub."""
  user = user_pb2.User(username=username)
  response = stub.CheckUser(user)
  return response

def run():
  """Runs the client application."""
  # Replace 'localhost:50051' with your server address.
  with grpc.insecure_channel('localhost:50051') as channel:
    stub = user_pb2_grpc.UserServiceStub(channel)

    username = "test"

    response = check_user(stub, username)

    if response.success:
      print(f"User {response.user_id} exists")
      return
    else:
      print(f"No user {username}")

if __name__ == '__main__':
  begin_time = time.time()
  for i in range(10000):
      run()
  timer_after = time.time()
  total_time = timer_after - begin_time
  avg_time = total_time/10000

  print("total_time: ", total_time, "s")
  print("avg_time: ", avg_time*1000, "ms")


