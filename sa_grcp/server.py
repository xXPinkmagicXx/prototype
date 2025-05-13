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

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
