import grpc
from . import user_pb2
from . import user_pb2_grpc
import string
import random
import sys

def delete_user(stub, username):
  """Creates a user using the gRPC stub."""
  user = user_pb2.User(username=username)
  response = stub.DeleteUser(user)
  return response

def run():
  """Runs the client application."""
  # Replace 'localhost:50051' with your server address.
  with grpc.insecure_channel('localhost:50051') as channel:
    stub = user_pb2_grpc.UserServiceStub(channel)
    username = sys.argv[1]
    response = delete_user(stub, username)

    if response.success:
      print(f"User created successfully! User ID: {response.user_id}")
    else:
      print(f"Failed to delete user. Error: {response.error_message}")


if __name__ == '__main__':
  run()
