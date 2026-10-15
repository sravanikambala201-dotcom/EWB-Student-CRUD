# Student Database CRUD Application

## Project Overview
A Python backend application to manage student records using FastAPI and SQLite.

## Technologies Used
- Python
- FastAPI
- SQLite
- Uvicorn

## Features
- Create student records
- List all students
- Retrieve student details by ID
- Update student details
- Delete student records
- Validate input and handle missing student records

## Installation
Create a virtual environment:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run the Application

```powershell
python -m uvicorn main:app --reload
```

Open the API documentation at http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /students | Create a student |
| GET | /students | List all students |
| GET | /students/{student_id} | Retrieve a student |
| PUT | /students/{student_id} | Update a student |
| DELETE | /students/{student_id} | Delete a student |

## Database
SQLite database file `students.db` is created automatically.

## Testing
Use the interactive Swagger documentation at `/docs` to test the endpoints.

## Internship Assignment
EWB Edu Tech Pvt. Ltd. — Python Backend Development