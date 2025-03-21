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

    username = sys.argv[1]

    response = check_user(stub, username)

    if response.success:
      print(f"User {response.user_id} exists")
      return
    else:
      print(f"No user {username}")

if __name__ == '__main__':
    run()


