from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime, timedelta

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_user_db = {
    "admin": {
        "password": pwd_context.hash("123456"),
        "failed_attempts": 0,
        "lock_until": None
    }
}

class LoginRequest(BaseModel):
    username: str
    password: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/login")
def login(user: LoginRequest):
    if len(user.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    if user.username not in fake_user_db:
        raise HTTPException(status_code=400, detail="User not found")

    db_user = fake_user_db[user.username]

    if db_user["lock_until"]:
        if datetime.now() < db_user["lock_until"]:
            remaining = (db_user["lock_until"] - datetime.now()).seconds
            raise HTTPException(
                status_code=403,
                detail=f"Account locked. Try again in {remaining} seconds"
            )
        else:
            db_user["failed_attempts"] = 0
            db_user["lock_until"] = None

    if not verify_password(user.password, db_user["password"]):
        db_user["failed_attempts"] += 1

        if db_user["failed_attempts"] >= 3:
            db_user["lock_until"] = datetime.now() + timedelta(minutes=2)
            raise HTTPException(
                status_code=403,
                detail="Account locked for 2 minutes due to multiple failed attempts"
            )

        raise HTTPException(status_code=400, detail="Incorrect password")

    db_user["failed_attempts"] = 0
    print(fake_user_db)

    return {"message": "Login successful"}