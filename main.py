from fastapi import FastAPI, Query
from enum import Enum
from typing import Optional
from pydantic import BaseModel

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
@app.get("/users_all")
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


# Pydantic model for user data
class User(BaseModel):
    username: str
    password : str
    type: AccessType  # User type must be one of: admin, user, superadmin
    salary: int
    tax: float

# Create a new user using POST method
@app.post("/users")
async def create_user(user: User):
    user_dict = user.model_dump()  # Convert Pydantic model to dictionary
    if user.tax:
        salary_with_tax = user.salary + user.tax  # Calculate salary including tax
        user_dict.update({"salary_with_tax": salary_with_tax})  # Add to response
    return user_dict  # Return full user data as response

# Update user using PUT method and support optional query string
@app.put("/users/{user_id}")
async def create_user_with_put_method(user_id: int, user: User, optional_query: Optional[str] = None):
    result = {"user_id": user_id, **user.model_dump()}  # Merge user_id with user data

    if optional_query:
        result.update({"optional_query": optional_query})  # Include optional query in result
    
    return result  # Return combined result

# ---------------------------

# Read all users with optional query string for filtering or testing
@app.get("/users")
async def read_users(
    optional_query : Optional[str] = Query(
        None,
        min_length=2,  # Minimum 2 characters required
        max_length=10,  # Maximum 10 characters allowed
        title="Example for query",  # Title shown in Swagger docs
        description="This is a example for query string",  # Description for documentation
        alias="user_query",  # Query parameter expected as "user_query" in URL
    )
):
    results = {"users": ["Alice", "Bob"]}  # Simulated user list
    if optional_query:
        results.update({"optional_query": optional_query})  # Include query in response if provided
    return results  # Return user list (and query if given)

# Hidden query parameter example — not shown in Swagger documentation
@app.get("/users_hidden")
async def hidden_user_query(
    hidden_query: Optional[str] = Query(
        None,
        include_in_schema=False  # Hide from API documentation (Swagger UI)
    )
):
    if hidden_query:
        return({"hidden_query": hidden_query})  # Return the hidden query value if provided
    return({"hidden_query": "not found"})  # Default fallback response
