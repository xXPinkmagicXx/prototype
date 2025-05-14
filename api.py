from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
import logging

# Set logging level to CRITICAL to suppress logs
logging.getLogger("uvicorn.access").setLevel(logging.CRITICAL)
logging.getLogger("uvicorn.error").setLevel(logging.CRITICAL)
app = FastAPI()

# Define the data model
class User(BaseModel):
    user_id: Optional[int] = None
    name: str
    email: str
    password: str

    def to_dict(self):
        {
            "user_id" : self.user_id,
            "name" : self.name,
            "email" : self.email,
            "password" : self.password,
        }

class Response(BaseModel):
    status_code: int
    message: str
    data: Optional[User] = None

# In-memory database
# email is the key
users_db: Dict[str, User] = {}
user_id_counter = 1

@app.post("/create_user/", response_model=Response)
def create_user(user: User):
    global user_id_counter
    user.user_id = user_id_counter
    users_db[user.email] = user
    user_id_counter += 1
    return Response(status_code=200, message="User created successfully", data=user)


@app.get("/users/{user_email}", response_model=User)
def get_user(user_email: str):
    if user_email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_email]

@app.get("/ok", response_model=Response)
def ok():
    return Response(status_code=200, message="OK")


# To run the API, use: `uvicorn script_name:app --reload`