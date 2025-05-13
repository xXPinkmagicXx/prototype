import grpc
from . import user_pb2
from . import user_pb2_grpc
import string
import random
import sys

def run():
  """Runs the client application."""
  # Replace 'localhost:50051' with your server address.
  with grpc.insecure_channel('localhost:50051') as channel:
    stub = user_pb2_grpc.UserServiceStub(channel)
    response = ok(stub)

    if response.success:
      print(f"User created successfully! User ID: {response.user_id}")
    else:
      print(f"Failed to delete user. Error: {response.error_message}")



def ok(stub):
  """Creates a user using the gRPC stub."""
  user = user_pb2.User()
  response = stub.Ok(user)
  return response