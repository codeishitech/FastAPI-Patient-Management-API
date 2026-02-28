# FastAPI Patient Management API

A simple FastAPI project to manage patient data using REST APIs.  
This project demonstrates request validation, path/query parameters, computed fields (BMI), and JSON-based persistence.

## Features

- Create a patient record
- View all patients
- View a single patient by ID
- Update patient details
- Sort patients by age
- Automatic BMI calculation using height and weight
- Input validation with Pydantic models

## Tech Stack

- Python
- FastAPI
- Pydantic
- Uvicorn

## Project Structure

```bash
.
├── main.py
└── patient.json
