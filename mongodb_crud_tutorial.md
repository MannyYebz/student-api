## MongoDB CRUD Operations Tutorial

## Scenario
We are building a **Student Course Enrollment System** where we:
- Store students
- Enroll them in courses
- Update their information
- Remove records when needed

---

## ⚙️ Step 1: Setup

### Install dependencies
```bash
pip install pymongo
```

### Start MongoDB server
```bash
mongod

mongoosh
```

## Create DB and Collection
```bash
show dbs
show collections

# create db
use student_db # automatically creates a db

# create collection
db.createCollection("student")

# insert
db.student.insertOne({ "name": "Theo", "age": 26, "courses": ["AI", "Data Science"], "graduated": false })

db.student.find()
db.student.find().pretty()
```

---

## 🔌 Step 2: Connect to MongoDB

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["school_db"]       # Database
collection = db["students"]    # Collection
```

---

## 🟢 CREATE (Insert Data)

### Insert one student
```python
student = {
    "name": "Theo",
    "age": 26,
    "courses": ["AI", "Data Science"],
    "graduated": False
}

result = collection.insert_one(student)
print("Inserted ID:", result.inserted_id)
```

### Insert multiple students
```python
students = [
    {"name": "Alice", "age": 22, "courses": ["Math"], "graduated": False},
    {"name": "Bob", "age": 24, "courses": ["Physics"], "graduated": True}
]

collection.insert_many(students)
```

---

## 🔵 READ (Query Data)

### Get all students
```python
for student in collection.find():
    print(student)
```

### Find one student
```python
student = collection.find_one({"name": "Theo"})
print(student)
```

### Query with condition
```python
for student in collection.find({"graduated": False}):
    print(student)
```

---

## 🟡 UPDATE (Modify Data)

### Update one student
```python
collection.update_one(
    {"name": "Theo"},
    {"$set": {"age": 27}}
)
```

### Add a course
```python
collection.update_one(
    {"name": "Theo"},
    {"$push": {"courses": "Machine Learning"}}
)
```

### Update multiple students
```python
collection.update_many(
    {"graduated": False},
    {"$set": {"status": "active"}}
)
```

---

## 🔴 DELETE (Remove Data)

### Delete one student
```python
collection.delete_one({"name": "Bob"})
```

### Delete multiple students
```python
collection.delete_many({"graduated": True})
```

---

## 🧪 Real-World Functions

```python
def enroll_student(name, course):
    collection.update_one(
        {"name": name},
        {"$push": {"courses": course}}
    )

def graduate_student(name):
    collection.update_one(
        {"name": name},
        {"$set": {"graduated": True}}
    )

def get_active_students():
    return list(collection.find({"graduated": False}))
```

---

## 🧱 Example Document

```json
{
  "_id": "661...",
  "name": "Theo",
  "age": 27,
  "courses": ["AI", "Data Science", "Machine Learning"],
  "graduated": false,
  "status": "active"
}
```

---

## ⚡ Pro Tips

- MongoDB is schema-less, but keep a consistent structure
- Use indexes for performance:
```python
collection.create_index("name")
```
- Use operators like:
  - $set → update fields
  - $push → add to arrays
  - $inc → increment values
- Always validate input in real applications

---

# Assignment
🏦 Assignment: Building a Simple Banking System with PyMongo

🎯 Objective

Learn how to use PyMongo to:

Connect to MongoDB
Create a database and collection
Perform full CRUD operations

📘 Scenario

You are building a basic banking system where customer accounts are stored in a database.

Each customer account should include:

account_number (string)
name (string)
balance (float)
account_type (e.g., “savings”, “checking”)

🧱 Tasks

1. Setup

Install PyMongo
Connect to your local MongoDB instance

2. Create Database and Collection

Create a database called: bank_db
Create a collection called: accounts

3. Insert Data (CREATE)

Insert at least 5 customer accounts.
{
"account_number": "ACC1001",
"name": "John Doe",
"balance": 1500.0,
"account_type": "savings"
}


4. Read Data (READ)

Write queries to:

Retrieve all accounts
Find one account by account_number
Find all accounts with balance greater than 1000

5. Update Data (UPDATE)

Implement:

Deposit money into an account (increase balance)
Withdraw money from an account (decrease balance)
Change account type (e.g., savings → checking)

6. Delete Data (DELETE)

Delete one account using account_number
Delete all accounts with balance less than 500