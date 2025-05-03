from fastapi import FastAPI

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