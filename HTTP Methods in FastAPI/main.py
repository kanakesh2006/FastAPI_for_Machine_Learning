from fastapi import FastAPI
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as file:
        data = json.load(file)
    return data

@app.get("/")
def hello():
    return {'message':'Patient Mangement System API'}

@app.get('/about')
def about():
    return {'meassage':'A fully functional API to manage your patient records'}

@app.get('/view')
def view():
    data = load_data()
    return data
