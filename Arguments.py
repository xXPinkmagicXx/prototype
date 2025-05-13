class Arguments:
    
    def __init__(self, grpc: bool, rest: bool):
        self.grpc = grpc
        self.rest = rest
        self.n_users = 0
        self.secure = False

    def __str__(self):
        return f"Arguments(grpc={self.grpc}, rest={self.rest})"