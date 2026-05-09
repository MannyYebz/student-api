from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
import os
import secrets
import uvicorn
from dotenv import load_dotenv

load_dotenv(".env", override=True)

app = FastAPI()

# -----------------------------
# Database
# -----------------------------
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["school_db"]
students = db["students"]
users = db["users"]

# Force DB creation
if "students" not in db.list_collection_names():
    students.insert_one({"init": True})
    students.delete_one({"init": True})

# Force DB creation
if "users" not in db.list_collection_names():
    users.insert_one({"init": True})
    users.delete_one({"init": True})
# -----------------------------
# Security
# -----------------------------
security = HTTPBearer()


# -----------------------------
# Models
# -----------------------------
class Student(BaseModel):
    name: str
    age: int
    course: str


class LoginRequest(BaseModel):
    username: str
    password: str


# -----------------------------
# Helpers
# -----------------------------
def serialize(student):
    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "age": student["age"],
        "course": student["course"],
    }


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    user = users.find_one({"token": token})

    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return user


# -----------------------------
# Public route
# -----------------------------
@app.get("/")
def root():
    return {
        "message": "Welcome to the Secure Student API by Manny",
        "version": "0.1.0",
        "docs": "/docs",
    }


# -----------------------------
# Login route
# -----------------------------
@app.post("/login")
def login(data: LoginRequest):
    user = users.find_one({"username": data.username, "password": data.password})

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    new_token = secrets.token_hex(16)

    users.update_one({"_id": user["_id"]}, {"$set": {"token": new_token}})

    return {"access_token": new_token, "token_type": "bearer"}


# -----------------------------
# Protected routes
# -----------------------------
@app.get("/v2/students")
def get_students(user=Depends(verify_token)):
    return [serialize(s) for s in students.find()]


@app.post("/v2/students")
def create_student(student: Student, user=Depends(verify_token)):
    result = students.insert_one(student.dict())
    new_student = students.find_one({"_id": result.inserted_id})
    return serialize(new_student)


@app.put("/v2/students/{student_id}")
def update_student(student_id: str, student: Student, user=Depends(verify_token)):
    result = students.update_one(
        {"_id": ObjectId(student_id)}, {"$set": student.dict()}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")

    updated = students.find_one({"_id": ObjectId(student_id)})
    return serialize(updated)


@app.get("/v2/students/{student_id}")
def get_student(student_id: str, user=Depends(verify_token)):
    try:
        student = students.find_one({"_id": ObjectId(student_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid student ID")

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return serialize(student)


@app.delete("/v2/students/{student_id}")
def delete_student(student_id: str, user=Depends(verify_token)):
    result = students.delete_one({"_id": ObjectId(student_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Deleted successfully"}


# -----------------------------
# Local run
# -----------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
