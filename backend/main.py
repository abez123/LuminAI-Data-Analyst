from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from app.api.middleware.auth_middleware import AuthMiddleware
from app.api.db.models import init_db
from app.dependencies.database import get_db

app = FastAPI()

# CORS setup (if frontend is hosted on a different domain)
# origins = ["http://localhost:3000"]  # Replace with actual frontend domain

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.on_event("startup")
async def startup_event():
    init_db()
    db = next(get_db())

# Add auth middleware
app.add_middleware(AuthMiddleware)
# Include API routes
app.include_router(api_router)


@app.get("/")
def read_root():
    return {"message": "Hello, Lumin API is running!"}
