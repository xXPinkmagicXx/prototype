class Arguments:
    
    def __init__(self, grpc: bool, rest: bool, secure: bool):
        self.grpc = grpc
        self.rest = rest
        self.n_users = 0
        self.secure = secure

    def __str__(self):
        return f"Arguments(grpc={self.grpc}, rest={self.rest})"