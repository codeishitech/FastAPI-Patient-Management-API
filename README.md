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

├── main.py
└── patient.json

## API Endpoints
GET / - Welcome message
GET /about - About this API
GET /view - View all patients
GET /patient/{patient_id} - View one patient
GET /sort?sort_by=age&order=asc|desc - Sort patients
POST /create - Create a new patient
PUT /edit/{patient_id} - Update an existing patient

## Request Models
Create Patient (POST /create)
## Required fields:
id (string)
name (string)
city (string)
age (int, > 0 and < 100)
gender (male or female)
weight (int, > 0)
height (int, > 0)
medical_history (list of strings)

## Update Patient (PUT /edit/{patient_id})
All fields optional:

name
city
age
gender
weight
height
medical_history

## How to Run Locally
1. Clone the repository

git clone <your-repo-url>
cd <your-repo-folder>

2. Install dependencies
   pip install fastapi uvicorn

3. Start the server
  uvicorn main:app --reload

4. Open docs in browser


Notes
Data is stored in patient.json.
This is a learning/demo project and not intended for production use.




