import pandas as pd
from fastapi import FastAPI
import pickle
import joblib
from pydantic import BaseModel
from fastapi.responses import JSONResponse

with open('C:/Users/td/implement_scoring_loan/api/explainer.pkl', 'rb') as f:
    explainer = pickle.load(f)
with open('C:/Users/td/implement_scoring_loan/api/selected_feature_names.pkl', 'rb') as f:
    features = list(pickle.load(f))

model_saved = joblib.load('C:/Users/td/implement_scoring_loan/api/scoring_loan.joblib')

data_df = pd.read_csv('C:/Users/td/implement_scoring_loan/api/data_cleaned.csv')
class User_input(BaseModel):
    customer : int
app = FastAPI()

@app.post("/local_importance")
def process_data(input:User_input):
    index_client = data_df[data_df['SK_ID_CURR'] == input.customer].index[0]
    data_customer = data_df[features].values[index_client]
    exp = explainer.explain_instance(data_customer, model_saved.set_params(selector=None).predict_proba, num_features=5, num_samples=5)
    return JSONResponse(content={"result": exp.as_html()})
