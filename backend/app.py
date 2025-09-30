from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
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

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/login")
@db_session
async def login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    user = User.get(username=username)
    if not user or not user.verify_password(password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    
    token_data = {"sub": user.username, "role": user.role}
    access_token = create_access_token(token_data)

    return {
    "username": user.username,
    "role": user.role,
    "access_token": access_token,
    "token_type": "bearer"
    }