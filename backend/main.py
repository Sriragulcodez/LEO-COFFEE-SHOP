from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

app = FastAPI(title="Leo Coffee Shop Backend")

# -------------------------------
# Database
# -------------------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["leo_coffee_shop"]
user_collection = db["users"]

# -------------------------------
# Security / JWT
# -------------------------------
SECRET_KEY = "leo_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -------------------------------
# Models
# -------------------------------
class User(BaseModel):
    username: str
    password: str

# -------------------------------
# Utility Functions
# -------------------------------
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")

# -------------------------------
# Routes
# -------------------------------
@app.get("/")
def root():
    return {"message": "FastAPI is running!"}

# User Registration
@app.post("/register")
def register(user: User):
    if user_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")

    user_data = {
        "username": user.username,
        "password": hash_password(user.password)
    }
    user_collection.insert_one(user_data)
    return {"message": "User registered successfully"}

# User Login
@app.post("/login")
def login(user: User):
    db_user = user_collection.find_one({"username": user.username})

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    token = create_access_token({"sub": user.username})
    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "expires_in_days": ACCESS_TOKEN_EXPIRE_DAYS
    }

# Protected Get Coffee (Query Parameter)
@app.get("/get-coffee")
def get_coffee(token: str):
    """
    Pass your JWT token directly in the query parameter:
    Example: /get-coffee?token=<YOUR_ACCESS_TOKEN>
    """
    username = verify_token(token)
    return {"message": "Coffee served ☕", "user": username}
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

app = FastAPI(title="Leo Coffee Shop Backend")

# -------------------------------
# Database
# -------------------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["leo_coffee_shop"]
user_collection = db["users"]
pass_collection = db["passes"]  # new collection for monthly passes

# -------------------------------
# Security / JWT
# -------------------------------
SECRET_KEY = "leo_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -------------------------------
# Models
# -------------------------------
class User(BaseModel):
    username: str
    password: str

# -------------------------------
# Utility Functions
# -------------------------------
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")

# -------------------------------
# Routes
# -------------------------------
@app.get("/")
def root():
    return {"message": "FastAPI is running!"}

# User Registration
@app.post("/register")
def register(user: User):
    if user_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    user_collection.insert_one({
        "username": user.username,
        "password": hash_password(user.password)
    })
    return {"message": "User registered successfully"}

# User Login
@app.post("/login")
def login(user: User):
    db_user = user_collection.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    token = create_access_token({"sub": user.username})
    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "expires_in_days": ACCESS_TOKEN_EXPIRE_DAYS
    }

# -------------------------------
# Monthly Pass
# -------------------------------
@app.post("/buy-pass")
def buy_pass(token: str):
    """
    User buys a monthly pass (30 coffees/month)
    """
    username = verify_token(token)
    now = datetime.utcnow()
    existing_pass = pass_collection.find_one({"username": username})

    if existing_pass:
        # Extend existing pass if expired or reset remaining coffees
        if existing_pass["end_date"] < now:
            pass_collection.update_one(
                {"username": username},
                {"$set": {
                    "start_date": now,
                    "end_date": now + timedelta(days=30),
                    "remaining_coffees": 30
                }}
            )
            return {"message": "Monthly pass renewed! 30 coffees added."}
        else:
            return {"message": "You already have an active monthly pass."}
    else:
        # Create new pass
        pass_collection.insert_one({
            "username": username,
            "start_date": now,
            "end_date": now + timedelta(days=30),
            "remaining_coffees": 30
        })
        return {"message": "Monthly pass purchased! 30 coffees added."}

# Get Coffee (with Pass Check)
@app.get("/get-coffee")
def get_coffee(token: str):
    username = verify_token(token)
    user_pass = pass_collection.find_one({"username": username})
    now = datetime.utcnow()

    if not user_pass or user_pass["end_date"] < now:
        raise HTTPException(status_code=403, detail="No active monthly pass. Please buy one.")

    if user_pass["remaining_coffees"] <= 0:
        raise HTTPException(status_code=403, detail="You have used all coffees this month.")

    # Decrement remaining coffees
    pass_collection.update_one(
        {"username": username},
        {"$inc": {"remaining_coffees": -1}}
    )

    return {
        "message": "Coffee served ☕",
        "remaining_coffees": user_pass["remaining_coffees"] - 1
    }
