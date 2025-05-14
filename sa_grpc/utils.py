import grpc
from . import user_pb2_grpc

def get_trusted_certificate():
   with open('./server.crt', 'rb') as f:
      trusted_certs = f.read()
   return trusted_certs

def create_channel_credentials() -> grpc.ChannelCredentials:
   trusted_certs = get_trusted_certificate()
   credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
   return credentials

def create_secure_channel()-> grpc.Channel:
   credentials = create_channel_credentials()
   return grpc.secure_channel('localhost:50051', credentials=credentials)

def create_insecure_channel():
   return grpc.insecure_channel('localhost:50051') 

def create_secure_stub():
   with create_secure_channel() as channel:
      stub = _create_stub(channel)
      return stub

def create_secure_stub_and_run(function: callable) -> None:
   with create_secure_channel() as channel:
      stub = _create_stub(channel)
      function(stub)

def create_insecure_stub():
   with create_insecure_channel() as channel:
      stub = _create_stub(channel)
      return stub

def _create_stub(channel):
   return user_pb2_grpc.UserServiceStub(channel)