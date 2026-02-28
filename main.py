from fastapi import FastAPI, Path, HTTPException, Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import List, Annotated, Literal, Optional

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(...,description="Unique identifier for the patient",examples=["p001","p002"])]
    name: Annotated[str, Field(...,description="Name of the patient")]
    city: Annotated[str, Field(...,description="City of residence of the patient")]
    age: Annotated[int, Field(..., gt=0, lt=100, description="Age of the patient in years")]
    gender: Annotated[Literal['male','female'] , Field(...,description="Gender of the patient")]   
    weight: Annotated[int, Field(..., gt=0, description="Weight of the patient in kg")] 
    height: Annotated[int, Field(..., gt=0, description="Height of the patient in cm")]
    medical_history: List[str]
    
    @computed_field
    @property
    def bmi(self)-> float:
        bmi = self.weight / ((self.height/100) ** 2)
        return round(bmi,2)


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None)]
    gender: Annotated[Optional[Literal['male','female']], Field(default=None)]   
    weight: Annotated[Optional[int], Field(default=None)] 
    height: Annotated[Optional[int], Field(default=None)]
    medical_history: Annotated[Optional[List[str]], Field(default=None)]
    
    
def save_data(data):
    with open('patient.json','w') as f:
        json.dump(data,f)

def load_data():
    with open('patient.json','r') as f:
        data = json.load(f)
    return data

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/")
def hello():
    return {"message": "patient management system."}

@app.get("/about")
def about():
    return{"message": "This is a simple FastAPI application."}

@app.get("/patient/{patient_id}")
def view_patients(patient_id: str = Path(..., description='id of patient', example='p001')):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get('/sort')
def sort_patient(sort_by: str= Query(...,description='sort on basis of order, age'), order: str = Query('asc', description='sort in ascending or descending order')):
    valid_fields = ['age']
    if sort_by not in valid_fields:
       raise HTTPException(status_code=400, detail=f'Invalid chose from {valid_fields}')
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='invaild order')
    data  = load_data()
    sort_order = True if order=='desc' else False
    
    sorted_data = sorted(data.values(),key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):
    #load existing data 
    data = load_data()
    #check if patient id already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient with this id already exists')
    #if not add patient to data and save to json file
    data[patient.id]= patient.model_dump(exclude=['id'])
    save_data(data)
        
    return JSONResponse(content={"message": "Patient created successfully"}, status_code=201)

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient id not found in database.")
    
    patient_existing_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    
    for key,value in updated_patient_info.items():
        patient_existing_info[key] = value
    
    # Handle case sensitivity for gender field - convert to lowercase
    if 'gender' in patient_existing_info and patient_existing_info['gender']:
        patient_existing_info['gender'] = patient_existing_info['gender'].lower()
    
    # Create pydantic object to recalculate computed field (bmi)
    patient_existing_info['id'] = patient_id
    patient_pydantic_obj = Patient(**patient_existing_info)
    patient_existing_info = patient_pydantic_obj.model_dump(exclude='id')

    data[patient_id] = patient_existing_info
    save_data(data)
    
    return JSONResponse(content={"message": "Patient information updated successfully"}, status_code=200)

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data =load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient id not found in database.")
    
    del data[patient_id]
    save_data(data)
    return JSONResponse(content={"message": "Patient information deleted successfully"}, status_code=200)

