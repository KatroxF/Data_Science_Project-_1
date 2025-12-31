import joblib
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Load the model (only once when server starts)
model = joblib.load("model.pkl")
class Model_input(BaseModel):
    age: int
    bmi: int
    children: int
    smoker_encoded: int
@app.post("/predict")
def predict(data:Model_input):
      features = [[
        data.age,
        data.bmi,
        data.children,
        data.smoker_encoded
    ]]
      prediction = model.predict(features)[0]
      
      return{
           'prediction':int(prediction)
      }