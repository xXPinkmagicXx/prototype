from sa_grpc import server
import threading

def start_grpc_server():
    # Start the gRPC server
    server.serve()

def main():


    # Run the server in a separate process
    # Run the server in a background thread
    start_grpc_server()
    
    # server_thread = threading.Thread(target=start_grpc_server, daemon=True)
    # server_thread.start()


    print("Server is running in the background...")


if __name__ == "__main__":
    main()

