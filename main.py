import send_requests as rest
from sa_grpc import run_create_user_experiment_insecure, run_create_user_experiment_secure
from sa_grpc.check_user import run_get_user_experiment_insecure, run_get_user_experiment_secure
from Arguments import Arguments
import argparse
import sys
import start_servers as server
import threading
import time
import grpc
from sa_grpc import call_grpc
import uvicorn
import requests
import constants as c
from Result import Result
import urllib3
# To supress the certificate warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    
def run_rest_get(n_users):

    print(f"Now getting {n_users} users.")
    avg_response_time_get_users, requests_pr_sec_get_users = rest.get_users(n_users, users_created=True)
    print("Get users: avg response time (ms):  ", avg_response_time_get_users, "; requests per second: ", requests_pr_sec_get_users)


def run_create_experiment(args: Arguments)->tuple[float, float]:
    
    # print(f"Now creating {n_users} users.")
    # avg_response_time_rest, requests_per_sec_rest = rest.post_create_users(n_users)
   avg_response_time, requests_per_sec = (0, 0)
   if args.grpc and args.secure:
      avg_response_time, requests_per_sec, users = run_create_user_experiment_secure(n_requests=args.n_users)
   if args.grpc and not args.secure:
      avg_response_time, requests_per_sec, users = run_create_user_experiment_insecure(n_requests=args.n_users)
   
   if args.rest and args.secure:
      avg_response_time, requests_per_sec = rest.post_create_users_secure(n_users=args.n_users)
   if args.rest and not args.secure:
      avg_response_time, requests_per_sec = rest.post_create_users(n_users=args.n_users)
   
   return avg_response_time, requests_per_sec

def start_sever_in_background(args: Arguments)->None:
   if args.grpc and not args.secure:
      grpc_server_thread = threading.Thread(target=server.start_grpc_insecure_server, daemon=True)
      grpc_server_thread.start()
      print(f"[Info] main.py - started server grpc secure: {args.secure}")


   if args.grpc and args.secure:
      grpc_server_thread = threading.Thread(target=server.start_grpc_secure_server, daemon=True)
      grpc_server_thread.start()
      print(f"[Info] main.py - started server grpc secure: {args.secure}")
   
   if args.rest and not args.secure:
      rest_server_thread = threading.Thread(target=server.start_rest_insecure_server, daemon=True)
      rest_server_thread.start()
      print(f"[Info] main.py - started server rest secure: {args.secure}")


   if args.rest and args.secure:
      rest_server_thread = threading.Thread(target=server.start_rest_secure_server, daemon=True)
      rest_server_thread.start()
      print(f"[Info] main.py - started server rest secure: {args.secure}")

def run_get_experiment(args: Arguments):

   avg_response_time, request_per_sec = None, None
   if args.rest and not args.secure:
      avg_response_time, request_per_sec = rest.get_users(args.n_users, False)

   if args.rest and args.secure:
      avg_response_time, request_per_sec = rest.get_users_secure(args.n_users, False)
   
   if args.grpc and not args.secure:
      avg_response_time, request_per_sec = run_get_user_experiment_insecure(args.n_users, False)
   
   if args.grpc and args.secure:
      avg_response_time, request_per_sec, usernames = run_get_user_experiment_secure(args.n_users, False)

   return avg_response_time, request_per_sec

def main(args: Arguments):

   start_sever_in_background(args)
   # Waiting for server to start
   starting = True
   while starting:
      if server.is_specified_server_healthy(args):
         starting = False
      else:
         print("[Info] Waiting for server to start...") 
      time.sleep(2)


   print("[Info] main.py: Running Experiment")

   if args.method == c.METHOD_CREATE:
      avg_response_time, request_per_second = run_create_experiment(args)
   elif args.method == c.METHOD_GET:
      avg_response_time, request_per_second = run_get_experiment(args)
   elif args.method == c.METHOD_DELETE:
      raise NotImplementedError("Delete")
   else:
      raise NotImplementedError(f"No experiment implemented with method: {args.method}")

   result = Result(args, avg_response_time, request_per_second)
   result.is_result_valid()
   result.save_experiment_to_file()

   # print("Request per second: ", request_per_second)
   # print("avg time per reqest: ", avg_time_per_request*1000, "ms")


if __name__ == "__main__":
    
   parser = argparse.ArgumentParser(description="Start gRPC and REST servers.")

   parser.add_argument("--grpc", "-g", action="store_true", help="Run gRPC server")
   parser.add_argument("--rest", "-r", action="store_true", help="Run REST server")
   parser.add_argument("--secure", "-s", action="store_true", help="With secure server")
   parser.add_argument("--n_users", "-n", type=int, default=10_000, help="Number of users to create")
   parser.add_argument("--method", "-m", type=str, default=c.METHOD_CREATE, help="Specify which method to test")

   args = parser.parse_args(sys.argv[1:])
   arguments = Arguments(grpc=args.grpc, rest=args.rest, secure=args.secure, method=args.method)
   arguments.n_users = args.n_users
   
   print("[Info] main.py - arguments: " , arguments)
   main(arguments)
   print("[Info] Experiment finished")