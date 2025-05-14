import grpc
from . import user_pb2
from . import user_pb2_grpc
from concurrent import futures

database = {}

class UserService(user_pb2_grpc.UserServiceServicer):
    
    
    def CreateUser(self, request, context):
        #print(f"Received user creation request: {request.username}, {request.email}")

        # Simulate user creation (replace with actual logic)
        user_id = request.username #In a real app, generate a unique ID.
        success = True
        error_message = ""

        if success:
            database[user_id] = request.email
            #print("current database:", database)
            return user_pb2.UserResponse(success=True, user_id=user_id)
        else:
            return user_pb2.UserResponse(success=False, error_message=error_message)
    
    def DeleteUser(self, request, context):
        user_id = request.username
        print(f"Received user deletion request: {request.username}")

        if request.username in database:
            removed = database.pop(request.username)
            print(f"Successfuly removed user {removed}")

        else:
            print("User doesnt exist")

    def CheckUser(self, request, context):
        user_id = request.username
        print("Checking user {request.username}")
        if request.username in database:
            print("User exist")
            return user_pb2.UserResponse(success=True, user_id=user_id)
        else:
            print("User doesn't exist")
            return user_pb2.UserResponse(success=False)
    
    def Ok(self, request, context):
        return user_pb2.Response(success=True)

def insecure_server():
    try: 
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
        print("Insecure server started on port 50051")
        server.wait_for_termination()

    except Exception as e:
        print(f"[Error] Server stopped unexpectedly: {e}")

def secure_server():
    try: 

        with open("./server.crt", "rb") as cert_file, open("./server.key", "rb") as key_file:
            server_credentials = grpc.ssl_server_credentials([(key_file.read(), cert_file.read())])

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
        # Add secure port with TLS
        server.add_secure_port('[::]:50051', server_credentials)
        server.start()
        
        print("Server started on port 50051")
        server.wait_for_termination()
        print("[info] Server terminated")

    except Exception as e:
        print(f"[Error] Server stopped unexpectedly: {e}")

if __name__ == '__main__':
    insecure_server()
