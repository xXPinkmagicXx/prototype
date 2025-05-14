
# API endpoints 
BASE_INSECURE_URL = "http://localhost:8000/"
BASE_SECURE_URL = "https://localhost:8000/"

REST_SECURE_OK_URL = "https://localhost:8000/ok"
REST_INSECURE_OK_URL = "http://localhost:8000/ok"

REST_SECURE_GET_URL = BASE_SECURE_URL + "get/"

# Certificate and private key
SERVER_PRIVATE_KEY_PATH =  "./server.key"
SERVER_CERTIFICATE_PATH =  "./server.crt"

# Server configuration
SERVER_PORT = 8000
SERVER_HOST = "127.0.0.1"

# Constants 

METHOD_CREATE = "create"
METHOD_GET = "get"
METHOD_DELETE = "delete"
