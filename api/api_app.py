from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

# class User_input(BaseModel):
#     id_client : int
df = pd.read_csv('C:/Users/td/implement_scoring_loan/notebook/data.csv')
app = FastAPI()

@app.post('/gender')
def prediction():
    result=df[df['SK_ID_CURR']==100002]['CODE_GENDER'].astype(float)
    return result
