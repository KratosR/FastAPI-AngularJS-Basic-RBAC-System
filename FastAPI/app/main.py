import os
from fastapi import FastAPI
from app.routes import auth, roles, users, students, instructors
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Role-Based API", version="1.0")

origins = [
    "http://192.46.211.180",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(roles.router)
app.include_router(users.router)
app.include_router(students.router)
app.include_router(instructors.router)

@app.get("/")
def root():
    return {"message": "Role-Based API with JWT"}
