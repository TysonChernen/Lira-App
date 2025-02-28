from fastapi import FastAPI
from app.database import engine, Base
from app import models  # Corrected import
from app.routers import users, subscriptions, dashboard, lesson  # Import subscriptions
from fastapi.middleware.cors import CORSMiddleware


# ✅ Define `app` before using it
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ✅ Allow frontend to connect
    allow_credentials=True,
    allow_methods=["*"],  # ✅ Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # ✅ Allow all headers
)


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
app.include_router(lesson.router)
