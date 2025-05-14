import send_requests as rest
from sa_grpc.create_user import run_create_user_experiment, run_create_user_experiment_secure
from Arguments import Arguments
import argparse
import sys
import start_servers as server
import threading
import time
import grpc
from sa_grpc import call_grpc

def run_rest_create(n_users: int):
    pass

    
def run_rest_get(n_users):

    print(f"Now getting {n_users} users.")
    avg_response_time_get_users, requests_pr_sec_get_users = rest.get_users(n_users, users_created=True)
    print("Get users: avg response time (ms):  ", avg_response_time_get_users, "; requests per second: ", requests_pr_sec_get_users)


def run_create_experiment(n_users: int, secure: bool):
    
    # print(f"Now creating {n_users} users.")
    # avg_response_time_rest, requests_per_sec_rest = rest.post_create_users(n_users)
    if secure:
      avg_respone_time_grcp, requests_per_sec_grcp = run_create_user_experiment_secure(n_requests=n_users)
    else:
      avg_respone_time_grcp, requests_per_sec_grcp = run_create_user_experiment(n_requests=n_users)
    
    
    # print("Create users: avg response time (ms): ", avg_response_time_rest, "; requests per second: ", requests_per_sec_rest)
    print("Create users: avg response time (ms): ", avg_respone_time_grcp, "; requests per second: ", requests_per_sec_grcp)
    return avg_respone_time_grcp, requests_per_sec_grcp


def main(args: Arguments):


    if args.grpc and not args.secure:
        grpc_server_thread = threading.Thread(target=server.start_grpc_insecure_server, daemon=True)
        grpc_server_thread.start()

    if args.grpc and args.secure:
        grpc_server_thread = threading.Thread(target=server.start_grpc_secure_server, daemon=True)
        grpc_server_thread.start()
    
    # Waiting for server to start
    starting = True
    while starting:
        if call_grpc.is_healthy(args.secure):
            starting = False
        time.sleep(1)

    avg_time_per_request, request_per_second = run_create_experiment(args.n_users, args.secure)
    
    print("Request per second: ", request_per_second)
    print("avg time per reqest: ", avg_time_per_request*1000, "ms")




if __name__ == "__main__":
    
    
    # How to parse arguments
    parser = argparse.ArgumentParser(description="Start gRPC and REST servers.")
    # How to parse short args 

    parser.add_argument("--grpc", "-g", action="store_true", help="Run gRPC server")
    parser.add_argument("--rest", "-r", action="store_true", help="Run REST server")
    parser.add_argument("--secure", "-s", action="store_true", help="With secure server")
    parser.add_argument("--n_users", "-n", type=int, default=10_000, help="Number of users to create")

    args = parser.parse_args(sys.argv[1:])
    arguments = Arguments(grpc=args.grpc, rest=args.rest, secure=args.secure)
    
    arguments.n_users = args.n_users
    print(arguments)
    main(arguments)
    
    print("[Info] Experiment finished")