from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='ID of the patient', example='P001')]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., description='Age of the patient', gt=0, le=120)]
    gender: Annotated[Literal['male', 'female'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., description='Height of the patient', gt=0)]
    weight: Annotated[float, Field(..., description='Weight of the patient', gt=0)]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'


def load_data():
    with open('patients.json', 'r') as file:
        data = json.load(file)
    return data

def save_data(data):
    with open('patients.json', 'w') as file:
        json.dump(data, file)


# http://localhost:8000/
@app.get("/")
def hello():
    return {'message':'Patient Mangement System API'}


# http://localhost:8000/about
@app.get('/about')
def about():
    return {'meassage':'A fully functional API to manage your patient records'}


# http://localhost:8000/view
@app.get('/view')
def view():
    data = load_data()
    return data


# http://localhost:8000/patient/P001
@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB', example='P001')):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='patient id not found')


# http://localhost:8000/sort?sort_by=height&order=desc
@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of Height, Weight, BMI'), order: str = Query('asc', description='Sort in Asc or Desc order')):
    
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field select from {valid_fields}")

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    
    data = load_data()

    sort_order = True if order == 'asc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data


# http://localhost:8000/create  
'''
{
    "id": "P006",
    "name": "Anish gupta",
    "city": "Mumbai",
    "age": 25,
    "gender": "male",
    "height": 2.5,
    "weight": 90.0
}
'''
@app.post('/create')
def create_patient(patient: Patient):

    # load existing data
    data = load_data()

    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')
    
    # add new patient to the database
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save into json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message':'Patient created Sucessfully'})
    



