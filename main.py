import send_requests as rest
from sa_grcp.create_user import run_create_user_experiment
from sa_grcp.server import serve

def run_rest_create(n_users: int):
    pass

    
def run_rest_get(n_users):

    print(f"Now getting {n_users} users.")
    avg_response_time_get_users, requests_pr_sec_get_users = rest.get_users(n_users, users_created=True)
    print("Get users: avg response time (ms):  ", avg_response_time_get_users, "; requests per second: ", requests_pr_sec_get_users)


def run_create_experiment(n_users: int):
    
    # print(f"Now creating {n_users} users.")
    avg_response_time_rest, requests_per_sec_rest = rest.post_create_users(n_users)
    avg_respone_time_grcp, requests_per_sec_grcp = run_create_user_experiment(n_requests=n_users)
    
    
    print("Create users: avg response time (ms): ", avg_response_time_rest, "; requests per second: ", requests_per_sec_rest)
    print("Create users: avg response time (ms): ", avg_respone_time_grcp, "; requests per second: ", requests_per_sec_grcp)



def main():

    n_users = 5000
    run_create_experiment(n_users)


def start_grcp_server():
    # Start the gRPC server
    serve()

if __name__ == "__main__":
    start_grcp_server()