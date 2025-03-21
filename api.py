from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import json

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

class Respose(BaseModel):
    status_code: int
    message: str
    data: Optional[User] = None

# In-memory database
# email is the key
users_db: Dict[str, User] = {}
user_id_counter = 1

@app.post("/create_user/", response_model=Respose)
def create_user(user: User):
    global user_id_counter
    user.user_id = user_id_counter
    users_db[user.email] = user
    user_id_counter += 1
    return Respose(status_code=200, message="User created successfully", data=user)

# @app.get("/users/", response_model=List[Dict[int, User]])
# def get_users():
#     return [users_db]

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@app.get("/users/{email}", response_model=User)
def get_user(user_email: str):
    if user_email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_email]

# @app.put("/users/{user_id}", response_model=User)
# def update_user(user_id: int, updated_user: User):
#     if user_id not in users_db:
#         raise HTTPException(status_code=404, detail="User not found")
#     users_db[user_id] = updated_user
#     return updated_user

# @app.delete("/users/{user_id}")
# def delete_user(user_id: int):
#     if user_id not in users_db:
#         raise HTTPException(status_code=404, detail="User not found")
#     del users_db[user_id]
#     return {"message": "User deleted successfully"}

# To run the API, use: `uvicorn script_name:app --reload`