import pandas as pd
from fastapi import FastAPI
import pickle
import joblib
from pydantic import BaseModel
app = FastAPI()


with open('explainer.pkl', 'rb') as f:
    explainer = pickle.load(f)

with open('selected_feature_names.pkl', 'rb') as f:
    features = list(pickle.load(f))

model_saved = joblib.load('scoring_loan.joblib')

data_df = pd.read_csv('df_api.csv',nrows=10)
class User_input(BaseModel):
    customer : int


@app.post("/local_importance")
def process_data(input:User_input):
    index_client = data_df[data_df['SK_ID_CURR'] == input.customer].index[0]
    data_customer = data_df[features].iloc[index_client].values

    exp = explainer.explain_instance(data_customer,
                                     model_saved.set_params(feature_selection=None).predict_proba,
                                     num_features=5,
                                     num_samples=5)
    probabilities = exp.predict_proba.tolist()
    feature_importance = [t[1] for t in exp.as_map()[1]]
    feature_names = [t[0] for t in exp.as_map()[1]]
    return {"probabilities": probabilities,'importances': feature_importance,'features':feature_names}


@app.post('/financial')
def prediction(input :User_input):
    income = data_df[data_df['SK_ID_CURR']==input.customer]['AMT_INCOME_TOTAL']
    credit = data_df[data_df['SK_ID_CURR']==input.customer]['AMT_CREDIT']
    annuity =data_df[data_df['SK_ID_CURR'] == input.customer]['AMT_ANNUITY']
    return {'income':income, 'credit':credit,'annuity': annuity}