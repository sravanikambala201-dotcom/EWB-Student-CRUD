
import sqlite3
from datetime import date
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, model_validator

app = FastAPI(title="Student Database CRUD API")

DB_PATH = Path(__file__).with_name("students.db")


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                email TEXT,
                phone TEXT
            )
        """)


initialize_database()


class Student(BaseModel):
    name: str
    date_of_birth: date
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

    @model_validator(mode="after")
    def check_contact(self):
        if not self.email and not self.phone:
            raise ValueError("Provide at least an email or phone number")
        return self


def student_dict(row):
    return dict(row)


@app.post("/students", status_code=201)
def create_student(student: Student):
    with get_connection() as connection:
        cursor = connection.execute(
            """INSERT INTO students (name, date_of_birth, email, phone)
               VALUES (?, ?, ?, ?)""",
            (
                student.name,
                student.date_of_birth.isoformat(),
                str(student.email) if student.email else None,
                student.phone,
            ),
        )
        student_id = cursor.lastrowid
        row = connection.execute(
            "SELECT * FROM students WHERE student_id = ?", (student_id,)
        ).fetchone()

    return student_dict(row)


@app.get("/students")
def get_students():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM students ORDER BY student_id"
        ).fetchall()
    return [student_dict(row) for row in rows]


@app.get("/students/{student_id}")
def get_student(student_id: int):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM students WHERE student_id = ?", (student_id,)
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student_dict(row)


@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    with get_connection() as connection:
        existing = connection.execute(
            "SELECT * FROM students WHERE student_id = ?", (student_id,)
        ).fetchone()

        if existing is None:
            raise HTTPException(status_code=404, detail="Student not found")

        connection.execute(
            """UPDATE students
               SET name = ?, date_of_birth = ?, email = ?, phone = ?
               WHERE student_id = ?""",
            (
                student.name,
                student.date_of_birth.isoformat(),
                str(student.email) if student.email else None,
                student.phone,
                student_id,
            ),
        )

        row = connection.execute(
            "SELECT * FROM students WHERE student_id = ?", (student_id,)
        ).fetchone()

    return student_dict(row)


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM students WHERE student_id = ?", (student_id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Student deleted successfully"}
