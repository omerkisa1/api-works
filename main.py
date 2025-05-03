from fastapi import FastAPI
from enum import Enum

app = FastAPI()


@app.get("/")
async def root():
    return{"message" :"root message"}

@app.post("/")
async def get():
    return{"message" :"post message"}

@app.put("/")
async def put():
    return{"message" :"put message"}

#------------------------------------------

@app.get("/users")
async def get_all_users():
    return {"message": "all users listed"}

@app.get("/users/current")
async def get_current_user():
    return {"message": "current user"}

@app.get("/users/{user_id}")
async def get_user(user_id : str):
    return {"message": f"user {user_id}"}


class AccessType(str, Enum):
    user = "user"
    admin = "admin"
    super_admin = "super_admin"

@app.get("/access/{user_type}")
async def get_user_by_role(user_type: AccessType):
    if user_type.value == "super_admin":
        return{"message": "you have full access"}
    if user_type.value == "admin":
        return{"message": "you have partial access"}
    else:
        return{"message": "normal user"}