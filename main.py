import send_requests as rest
import gRCP-client.check_user


def run_rest(n_users: int):


    print("running REST")
    
    print(f"Now creating {n_users} users.")
    avg_response_time_create_users, requests_pr_sec_create_users = rest.post_create_users(n_users)
    
    print(f"Now getting {n_users} users.")
    avg_response_time_get_users, requests_pr_sec_get_users = rest.get_users(n_users, users_created=True)

    print("Create users: avg response time (ms): ", avg_response_time_create_users, "; requests per second: ", requests_pr_sec_create_users)
    print("Get users: avg response time (ms):  ", avg_response_time_get_users, "; requests per second: ", requests_pr_sec_get_users)


def run_grcp(n_users: int):


def main():

    n_users = 5000
    
    run_rest(n_users)

if __name__ == "__main__":
    main()