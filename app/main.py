from typing import Union

from fastapi import FastAPI

import pickle

app = FastAPI()




def load_model():
    with open("../pickle_model.pkl", "rb") as f:
        return pickle.load(f)
    


@app.get("/")
def read_root():
    return {"Hello": "World"}




@app.get("/predict/{time}")
def predict(time: int):
    model = load_model()
    return {"time_id": time, "prediction": model.predict(time) }
