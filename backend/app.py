from fastapi import FastAPI, HTTPException, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from werkzeug.security import generate_password_hash
from models import User, File, Role
from pony.orm import db_session
import shutil
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import jwt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="http://localhost:5173",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/ping")
async def ping():
    return {"msg": "pong"}

@app.post("/login")
@db_session
def login(user_data: dict = Body(...)):
    username = user_data.get("username")
    password = user_data.get("password")

    user = User.get(username=username)
    if not user or not user.verify_password(password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token_data = {"sub": user.username, "role": user.role}
    access_token = create_access_token(token_data)

    return JSONResponse(content={
        "username": user.username,
        "role": user.role,
        "access_token": access_token,
        "token_type": "bearer"
    })