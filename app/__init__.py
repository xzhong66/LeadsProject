from fastapi import FastAPI

from .database import Base, engine
from .routes import leads

Base.metadata.create_all(bind=engine)
print("Database initialized.")

app = FastAPI()

app.include_router(leads.router)
