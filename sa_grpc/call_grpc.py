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


def ok(stub, username, email):
  """Creates a user using the gRPC stub."""
  user = user_pb2.User(username=username, email=email)
  response = stub.Ok(user)
  return response


def is_insecure_healthy() -> bool:
  try:
    with grpc.insecure_channel('localhost:50051') as channel:
      stub = user_pb2_grpc.UserServiceStub(channel)
      empty = user_pb2.EmptyRequest()
      response = stub.Ok(empty)

      return response.success
    
  except grpc.RpcError as e:
    print(f"[Error] call_grpc.py - Insecure Health check failed")
    return False
  
def is_secure_healthy() -> bool:
  
   with open('./server.crt', 'rb') as f:
      trusted_certs = f.read()

   with open('./server.key', 'rb') as f:
      private_key = f.read()

   credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
   try:
      with grpc.secure_channel('localhost:50051', credentials=credentials) as channel:
         stub = user_pb2_grpc.UserServiceStub(channel)
         empty = user_pb2.EmptyRequest()
         response = stub.Ok(empty)

         return response.success
      
   except grpc.RpcError as e:
      print(f"[Error] Health check failed {e}")
      return False
   except FileNotFoundError:
      print("[Error] Certificate file not found.")
      return False
  
def is_healthy(secure: bool)-> bool:
  if not secure:
    return is_insecure_healthy()
  return is_secure_healthy() 
