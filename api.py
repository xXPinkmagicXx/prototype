from fastapi import FastAPI, HTTPException, Request
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
    return Response(status_code=200, message="User created successfully", data=user.email)

@app.get("/users/", response_model=Response)
def get_user(request: Request):
    body = request.json()
    print(body)
    user_email = request.query_params['user_email']
    if user_email in users_db:
        return Response(status_code=200, message="User found", data=users_db[user_email])
    
    return Response(status_code=404, message="User not found", data=None)

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