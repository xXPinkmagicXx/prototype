# prototype
This contains the proto type for the course Software Architecture


# Environment

The code is develop with Python version 3.12.3

To run the code install the `requirments`

```bash
pip install -r requirements.txt
```


# Run the code

## Run the FastAPI

To start the application
```bash
uvicorn api:app --reload
```

Open another teminal

```bash
python send_requests.py
```
The output should be something like
```bash
running main
Now creating 5000 users.
Now getting 5000 users.
Create users: avg response time (ms):  2.6273900985717775 ; requests per second:  380.5068684495124
Get users: avg response time (ms):   1.2473440170288086 ; requests per second:  801.3403155317231
```

## Run grpc

# Development

## Add to grpc 

To add a new service to the grpc server, you need to do the following:

1. Add a new function in the `user.proto` file
2. Regenerate the grpc files with the command
```bash
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. user.proto
```


