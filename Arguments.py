class Arguments:
    
    def __init__(self, grpc: bool, rest: bool, secure: bool, method: str):
        self.grpc = grpc
        self.rest = rest
        self.n_users = 0
        self.secure = secure
        self.method = method

    def __str__(self):
        
      print_string = f"""Arguments( grpc={self.grpc}, rest={self.rest}, n_users={self.n_users},secure={self.secure},method={self.method})"""
      return print_string