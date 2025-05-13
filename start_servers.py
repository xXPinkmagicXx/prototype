from sa_grpc import server
import threading
import grpc
from sa_grpc import user_pb2_grpc
from sa_grpc import user_pb2
import time
import uvicorn
import requests
import argparse
import sys
from Arguments import Arguments


def do_grpc_health_check(current_uptime: float)-> bool:
    # Create a gRPC channel
    with grpc.insecure_channel('localhost:50051') as channel:
        # Create a stub (client)
        stub = user_pb2_grpc.UserServiceStub(channel)
        return check_grpc_server_health(stub, current_uptime)


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
    rest_server_thread = threading.Thread(target=lambda: uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True), daemon=True)
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

def start_rest_server():
    rest_server_thread = create_rest_server_thread()
    rest_server_thread.start()

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
        is_healthy = do_grpc_health_check(uptime)
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
        is_healthy = do_grpc_health_check(uptime)
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
        start_rest_server()
        return

    if args.rest and args.secure:
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
     
    args = parser.parse_args(sys.argv[1:])
    arguments= Arguments(grpc=args.grpc, rest=args.rest)

    
    main(arguments)


