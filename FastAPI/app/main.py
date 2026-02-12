import os
from fastapi import FastAPI
from app.routes import auth, roles, users, students, instructors
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Role-Based API", version="1.0")

# ─── CORS: Production Origins from ENV ─────────────────────
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
if not allowed_origins or allowed_origins == [""]:
    allowed_origins = [
        "http://localhost",
        "http://localhost:4200",
        "http://127.0.0.1:4200"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,# List of allowed origins
    allow_credentials=True,       # Allow cookies / Authorization headers
    allow_methods=["*"],          # Allow all HTTP methods (GET, POST, PATCH, DELETE, etc.)
    allow_headers=["*"],          # Allow all headers
)

app.include_router(auth.router)
app.include_router(roles.router)
app.include_router(users.router)
app.include_router(students.router)
app.include_router(instructors.router)

@app.get("/")
def root():
    return {"message": "Role-Based API with JWT"}