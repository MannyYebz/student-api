```
| Method | Endpoint            | Description      |
| ------ | ------------------- | ---------------- |
| GET    | `/v1/students`      | Get all students |
| GET    | `/v1/students/{id}` | Get one student  |
| POST   | `/v1/students`      | Create student   |
| PUT    | `/v1/students/{id}` | Update student   |
| DELETE | `/v1/students/{id}` | Delete student   |

```

```bash

# Insert records
curl -X POST http://localhost:8000/v1/students \
-H "Content-Type: application/json" \
-d '{
    "name":"Alice",
    "age":23,
    "course":"AI"
}'

# Production
curl -X POST https://student-api-v2.onrender.com/v1/students \
-H "Content-Type: application/json" \
-d '{
    "name":"Emmanuel",
    "age":53,
    "course":"Python and AI"
}'

# GET Student by ID
curl -X GET 'http://localhost:8000/v1/students/69f11c84b9ac80396d2807a5' \
--header 'Content-Type: application/json' \
--data '{
    "name":"John",
    "age":99,
    "course":"AML"
}'

# Update Student
curl -X PUT 'http://localhost:8000/v1/students/69f11c84b9ac80396d2807a5' \
--header 'Content-Type: application/json' \
--data '{
    "name":"John",
    "age":99,
    "course":"Python"
}'


# Delete Student by ID
curl -X DELETE 'http://localhost:8000/v1/students/69f11c84b9ac80396d2807a5' \
--header 'Content-Type: application/json'

```

## Deploy
```bash
# build command
pip install uv && uv sync

# start command
uv run uvicorn main:app --host 0.0.0.0 --port $PORT


# Render environment variable
MONGO_URI=your_mongodb_atlas_url
PORT=8000

```