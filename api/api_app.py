from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

df = pd.read_csv('C:/Users/td/implement_scoring_loan/notebook/data.csv')
class User_input(BaseModel):
    customer : int

app = FastAPI()

@app.post('/gender')
def prediction(input:User_input):
    result = df[df['SK_ID_CURR']==input.customer]['CODE_GENDER'].astype(float)
    return {'gender':result}

@app.post('/financial')
def prediction(input:User_input):
    income = df[df['SK_ID_CURR']==input.customer]['AMT_INCOME_TOTAL'].astype(float)
    credit = df[df['SK_ID_CURR']==input.customer]['AMT_CREDIT'].astype(float)
    annuity = df[df['SK_ID_CURR'] == input.customer]['AMT_ANNUITY'].astype(float)
    return {'income':income, 'credit':credit,'annuity': annuity}
