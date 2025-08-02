from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserLogin
from datetime import datetime, timedelta
import hashlib

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(db: Session, user: UserCreate):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = User(
        name=user.name,
        email=user.email,
        password=(user.password),
        gender=user.gender,
        age=user.age,
        access_token="dummy_access",
        refresh_token="dummy_refresh",
        access_token_expiry=datetime.utcnow() + timedelta(minutes=15),
        refresh_token_expiry=datetime.utcnow() + timedelta(days=7),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login_user(db: Session, credentials: UserLogin):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or user.password != (credentials.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

def get_users(db: Session):
    return db.query(User).all()

def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def update_user(db: Session, user_id: int, updates: dict):
    user = get_user(db, user_id)
    for key, value in updates.items():
        if hasattr(user, key):
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}
