from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd


class User_input(BaseModel):
    customer : int

app = FastAPI()

@app.post('/gender')
def prediction(input:User_input):
    # result = df[df['SK_ID_CURR']==input.customer]['CODE_GENDER'].astype(float)
    return {'gender':0}
