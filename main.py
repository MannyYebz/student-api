import os
import uvicorn
from bson import ObjectId
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv(".env", override=True)

app = FastAPI()

# ---------------------------
# Connect to REMOTE MongoDB
# ---------------------------
MONGO_URI = os.getenv("MONGO_URI")

# Create a new client and connect to the server
# tls=True, tlsCAFile=certifi.where()
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# ---------------------------
# Connect to local MongoDB
# ---------------------------

# MONGO_URI = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/?directConnection=true")
# client = MongoClient(MONGO_URI)


db = client["school_db"]
students_collection = db["students"]

# Force DB creation
if "students" not in db.list_collection_names():
    students_collection.insert_one({"init": True})
    students_collection.delete_one({"init": True})


# ---------------------------
# Pydantic Model
# ---------------------------
class Student(BaseModel):
    name: str
    age: int
    course: str


# ---------------------------
# Helper function
# {"_id":"69f146ad284889fb5dd7bd2a","name":"Trump","age":99,"course":"War"}
# ---------------------------
def student_serializer(student) -> dict:
    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "age": student["age"],
        "course": student["course"]
    }


# ---------------------------
# Root endpoint
# https://student-api-v2.onrender.com
# ---------------------------
@app.get("/")
def root():
    return {
        "message": "Welcome to the Student API",
        "version": "1.0",
        "docs": "/docs"
    }


# ---------------------------
# GET all students
# https://student-api-v2.onrender.com/v1/students
# ---------------------------
@app.get("/v1/students")
def get_students():
    students = students_collection.find()
    return [student_serializer(student) for student in students]


# ---------------------------
# POST create student
# https://student-api-v2.onrender.com/v1/students
# ---------------------------
@app.post("/v1/students")
def create_student(student: Student):
    result = students_collection.insert_one(student.model_dump())
    new_student = students_collection.find_one({"_id": result.inserted_id})
    return student_serializer(new_student)


# ---------------------------
# PUT update student
# https://student-api-v2.onrender.com/v1/students/69f949faf90e3610e6ff72d7
# ---------------------------
@app.put("/v1/students/{student_id}")
def update_student(student_id: str, student: Student):
    result = students_collection.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": student.model_dump()}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")

    updated_student = students_collection.find_one({"_id": ObjectId(student_id)})
    return student_serializer(updated_student)


# ---------------------------
# GET one student by ID
# https://student-api-v2.onrender.com/v1/students/69f949faf90e3610e6ff72d7
# ---------------------------
@app.get("/v1/students/{student_id}")
def get_student(student_id: str):
    student = students_collection.find_one({"_id": ObjectId(student_id)})

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student_serializer(student)


# ---------------------------
# DELETE student
# https://student-api-v2.onrender.com/v1/students/69f949faf90e3610e6ff72d7
# ---------------------------
@app.delete("/v1/students/{student_id}")
def delete_student(student_id: str):
    result = students_collection.delete_one({"_id": ObjectId(student_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Student deleted successfully"}


# ---------------------------
# Run application
# ---------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=os.getenv("PORT", 8000))
