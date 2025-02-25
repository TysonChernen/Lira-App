from fastapi import FastAPI
from app.database import engine, Base
from app import models  # Corrected import
from app.routers import users, subscriptions, dashboard  # Import subscriptions

# ✅ Define `app` before using it
app = FastAPI()

# ✅ Create database tables
Base.metadata.create_all(bind=engine)

# ✅ Include user routes
app.include_router(users.router)

@app.get("/")
def home():
    return {"message": "Welcome to Lira App!"}


app.include_router(users.router)
app.include_router(subscriptions.router)  # Register new subscription routes
app.include_router(dashboard.router) 
