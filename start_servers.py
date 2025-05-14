from sa_grpc import server
import threading
import grpc
from sa_grpc import user_pb2_grpc
from sa_grpc import user_pb2
import time
import uvicorn
from uvicorn import Config, Server
import requests
import argparse
import sys
from Arguments import Arguments
from sa_grpc import call_grpc


# def do_grpc_health_check(current_uptime: float)-> bool:
#     # Create a gRPC channel
#     with grpc.insecure_channel('localhost:50051') as channel:
#         # Create a stub (client)
#         stub = user_pb2_grpc.UserServiceStub(channel)
#         return check_grpc_server_health(stub, current_uptime)


def check_grpc_server_health(stub, current_uptime)-> bool:
    try:
        empty = user_pb2.EmptyRequest()
        response = stub.Ok(empty)
        if response.success:
            print("[Info] Server is healthy - Uptime: ", current_uptime, " seconds")
        else:
            print("[Error] Server is not responding correctly.")
            return False
    except grpc.RpcError as e:
        print(f"[Error] Health check failed: {e}")
        return False
    
    return True


base = "http://127.0.0.1:8000/" 
ok_url = base + "ok"

def check_rest_server_health(current_uptime):
    response = requests.get(ok_url)
    if response.status_code != 200:
        print("[Error] REST server is not healthy.")
        return False
    
    return True


def create_rest_server_thread()-> threading.Thread:
   def run_rest_server():
      try:
         uvicorn.run("api:app", host="127.0.0.1", port=8000)
      except Exception as e:
         print(f"[Error] - start_severs.py: REST server failed to start {e}")
         return
   rest_server_thread = threading.Thread(target=run_rest_server, daemon=True)
   return rest_server_thread

def create_rest_server_thread_secure()-> threading.Thread:
   def create_secure_rest_server():
      try:
         config = Config(
               "api:app", 
               host="127.0.0.1", 
               port=8000,  # Use a standard HTTPS port like 443 or 8443
               ssl_keyfile="./server.key",  # Path to your private key
               ssl_certfile="./server.crt"  # Path to your certificate
         )
         server = Server(config)
         server.run()
      except Exception as e:
         print(f"[Error] - start_servers.py: Secure REST server failed to start {e}")
         return
   rest_server_thread = threading.Thread(target=create_secure_rest_server, daemon=True)
   return rest_server_thread

def server_thread_creation(server_creation_function):
    server_thread = threading.Thread(target=server_creation_function, daemon=True)
    return server_thread

def create_grpc_server_thread()-> threading.Thread:
    grpc_server_thread = threading.Thread(target=server.insecure_server, daemon=True)
    return grpc_server_thread


# def do_health_checks(current_uptime)-> bool:
    
#     grpc_is_healthy = False
#     with grpc.insecure_channel('localhost:50051') as channel:
#         stub = user_pb2_grpc.UserServiceStub(channel)
#         grpc_is_healthy = check_grpc_server_health(stub, current_uptime)
    
#     # Check REST server health
#     # do a request to the REST server
#     rest_is_healthy = check_rest_server_health(current_uptime)

#     return rest_is_healthy and grpc_is_healthy

def is_rest_healthy():
      try:
         response = requests.get(ok_url)
         print(response)
         print(f"[Info] REST server health check response: {response.status_code}")
         if response.status_code == 200:
               return True
         else:
               print("[Error] - start_severs.py: REST server is not healthy.")
               return False
      except Exception as e:
         print(f"[Error] - start_severs.py:  REST server health check failed")
         return False  

def is_rest_secure_healthy():
   try:
      response = requests.get(ok_url, cert=("./server.crt", "./server.key") )
      print(response)
      print(f"[Info] Secure REST server health check response: {response.status_code}")
      if response.status_code == 200:
            return True
      else:
            print("[Error] - start_severs.py: Secure REST server is not healthy.")
            return False
   except Exception as e:
      print(f"[Error] - start_severs.py: Secure REST server health check failed")
      return False

def is_any_server_healthy():
   g_insec_health = call_grpc.is_insecure_healthy()
   if g_insec_health:
      return True
   g_sec_health = call_grpc.is_secure_healthy() 
   if g_sec_health:
      return True
   
   r_health = is_rest_healthy()
   if r_health:
      return True
   
   return False

def is_specified_server_healthy(args: Arguments):

   if args.rest and not args.secure:
      return is_rest_healthy()
   if args.rest and args.secure:
      return is_rest_secure_healthy()
   if args.grpc and not args.secure:
      return call_grpc.is_secure_healthy()
   if args.grpc and args.secure:
      return call_grpc.is_insecure_healthy()

   raise NotImplementedError(f"No Server health for {args}.")

def start_rest_insecure_server():
   uptime = 0
   sleep_time_sec = 5
   rest_server_thread = create_rest_server_thread()
   rest_server_thread.start()

   # Wait for the servers to start
   time.sleep(5)  # Adjust this as necessary to ensure the server is up
   while True:
      if not is_rest_healthy():
         print("[Error] Server is not healthy.")
         uptime += sleep_time_sec
      else: 
         # print("[Info] Server is healthy - Uptime: ", uptime, " seconds")
         uptime += sleep_time_sec
      time.sleep(sleep_time_sec)  # Adjust this as necessary to ensure the server is up

def start_rest_secure_server():
   uptime = 0
   sleep_time_sec = 5
   rest_server_thread = create_rest_server_thread_secure()
   rest_server_thread.start()

   # Wait for the servers to start
   time.sleep(5)  # Adjust this as necessary to ensure the server is up
   while True:
      if not is_rest_secure_healthy():
         uptime += sleep_time_sec
      else: 
         # print("[Info] Server is healthy - Uptime: ", uptime, " seconds")
         uptime += sleep_time_sec
      time.sleep(sleep_time_sec)  # Adjust this as necessary to ensure the server is up

def start_grpc_insecure_server():

   uptime = 0
   sleep_time_sec = 30
   # Run the server in a separate process
   # Run the server in a background thread
   # start_grpc_server()
   grpc_server_thread = server_thread_creation(server.insecure_server)
   grpc_server_thread.start()
   
   # Wait for the servers to start
   time.sleep(5)  # Adjust this as necessary to ensure the server is up
   while True:
      is_healthy = call_grpc.is_insecure_healthy()
      if not is_healthy:
         print("[Error] Server is not healthy.")
         break
      uptime += sleep_time_sec
      time.sleep(sleep_time_sec)  # Adjust this as necessary to ensure the server is up


def start_grpc_secure_server():
    uptime = 0
    sleep_time_sec = 30
    grpc_server_thread = server_thread_creation(server.secure_server)
    grpc_server_thread.start()
    
    # Wait for the servers to start
    time.sleep(5)  # Adjust this as necessary to ensure the server is up
    while True:
        is_healthy = call_grpc.is_secure_healthy()
        if not is_healthy:
            print("[Error] Server is not healthy.")
            break
        uptime += sleep_time_sec
        time.sleep(sleep_time_sec)  # Adjust this as necessary to ensure the server is up

def start_server_from_args(args: Arguments):
    if args.grpc and not args.secure:
        start_grpc_insecure_server()
        return
    
    if args.grpc and args.secure:
        start_grpc_secure_server()
        return

    if args.rest and not args.secure:
        start_rest_insecure_server()
        return

    if args.rest and args.secure:
        start_rest_secure_server()
        print("[Error] Secure REST server is not implemented yet.")
        return
    

def main(args:Arguments) -> None:
    
    start_server_from_args(args)

    print("[Error] No server started specified")
    return


if __name__ == "__main__":
    
    # How to parse arguments
    parser = argparse.ArgumentParser(description="Start gRPC and REST servers.")
    # How to parse short args 

    parser.add_argument("--grpc", "-g", action="store_true", help="Port for gRPC server")
    parser.add_argument("--rest", "-r", action="store_true", help="Port for gRPC server")
    parser.add_argument("--secure", "-s", action="store_true", help="With secure server")

    args = parser.parse_args(sys.argv[1:])
    arguments= Arguments(grpc=args.grpc, rest=args.rest, secure=args.secure)

    
    main(arguments)


