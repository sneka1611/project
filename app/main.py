from fastapi import FastAPI
from app.models.database import Base, engine
from app.routes import user_route

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_route.router)
