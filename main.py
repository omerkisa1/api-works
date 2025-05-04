from fastapi import FastAPI
from enum import Enum
from typing import Optional

app = FastAPI()

# Root endpoint - GET request
@app.get("/")
async def root():
    return {"message": "root message"}

# Root endpoint - POST request
@app.post("/")
async def get():
    return {"message": "post message"}

# Root endpoint - PUT request
@app.put("/")
async def put():
    return {"message": "put message"}

# ------------------------------------------

# Returns all users
@app.get("/users")
async def get_all_users():
    return {"message": "all users listed"}

# Returns the current (logged-in) user
@app.get("/users/current")
async def get_current_user():
    return {"message": "current user"}

# Returns a user based on user_id
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    return {"message": f"user {user_id}"}


# Enum for role-based access
class AccessType(str, Enum):
    user = "user"
    admin = "admin"
    super_admin = "super_admin"

# Returns access level message based on user role
@app.get("/access/{user_type}")
async def get_user_by_role(user_type: AccessType):
    if user_type.value == "super_admin":
        return {"message": "you have full access"}
    if user_type.value == "admin":
        return {"message": "you have partial access"}
    else:
        return {"message": "normal user"}

# Example database of player items (in-memory list)
db_player_items = [
    {"player_item": "sword"},
    {"player_item": "shield"},
    {"player_item": "armor"}
]

# Lists player items with optional pagination using skip and limit
@app.get("/player_items")
async def list_items(skip: int = 0, limit: int = 5):
    return {"player_items": db_player_items[skip: skip + limit]}  # fixed slice syntax

# Returns a single player item with query parameters
@app.get("/player_items/{player_item_id}")
async def get_item(
    player_item_id: int,  # fixed name to match the path param
    sample_query: str,
    optional_query: Optional[str] = None,
    short: bool = False
):
    item = {"player_item": player_item_id, "sample_query": sample_query}
    if optional_query:
        item.update({"optional_query": optional_query})
    if not short:
        item.update({"item_description": "Now you are seeing the full description of the item"})
    return item

# Returns a player item that belongs to a specific user
@app.get("/users/{user_id}/player_items/{player_item_id}")
async def get_user_item(
    user_id: int,
    player_item_id: str,
    optional_query: Optional[str] = None,
    short: bool = False
):
    item = {"user_id": user_id, "player_item_id": player_item_id}
    if optional_query:
        item.update({"optional_query": optional_query})
    if not short:
        item.update({"item_description": "Now you are seeing the full description of the item"})
    return item

# ---------------------------
