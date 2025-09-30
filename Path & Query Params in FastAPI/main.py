from fastapi import FastAPI, Path, Query, HTTPException
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as file:
        data = json.load(file)
    return data


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


