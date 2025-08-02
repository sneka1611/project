from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.schemas.user_schema import UserCreate, UserLogin, UserOut
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)

@router.post("/login", response_model=UserOut)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    return user_service.login_user(db, credentials)

@router.get("/", response_model=list[UserOut])
def get_all(db: Session = Depends(get_db)):
    return user_service.get_users(db)

@router.get("/{user_id}", response_model=UserOut)
def get_one(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user(db, user_id)

@router.put("/{user_id}", response_model=UserOut)
def update(user_id: int, updates: dict, db: Session = Depends(get_db)):
    return user_service.update_user(db, user_id, updates)

@router.delete("/{user_id}")
def delete(user_id: int, db: Session = Depends(get_db)):
    return user_service.delete_user(db, user_id)
