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

data_df = pd.read_csv('C:/Users/td/implement_scoring_loan/api/df_api.csv',nrows=10)
class User_input(BaseModel):
    customer : int
app = FastAPI()

@app.post("/local_importance")
def process_data(input:User_input):
    index_client = data_df[data_df['SK_ID_CURR'] == input.customer]
    data_customer = data_df[features].values[index_client]
<<<<<<< Updated upstream
    exp = explainer.explain_instance(index_client, model_saved.set_params(selector=None).predict_proba, num_features=5, num_samples=5)
    probabilities = model_saved.predict_proba(index_client)[0].tolist()
    html_explanation = exp.as_html(show_all=False)
    return JSONResponse(content={"result": {"probabilities": probabilities, "html_explanation": html_explanation}, "predict_proba": False})
=======
    exp = explainer.explain_instance(data_customer, model_saved.set_params(feature_selection=None).predict_proba, num_features=5, num_samples=5)
    probabilities = exp.predict_proba.tolist()
    feature_explanation = exp.as_map()
    feature_importance = [t[1] for t in feature_explanation[1]]
    feature_importance = [float(x) for x in feature_importance]
    feature_names = [t[0] for t in feature_explanation[1]]
    feature_names = [float(x) for x in feature_names]
    return {"probabilities": probabilities,'importances': feature_importance,'features':feature_names}

>>>>>>> Stashed changes

@app.post('/financial')
def prediction(input:User_input):
    income = data_df[data_df['SK_ID_CURR']==input.customer]['AMT_INCOME_TOTAL']
    credit = data_df[data_df['SK_ID_CURR']==input.customer]['AMT_CREDIT']
    annuity =data_df[data_df['SK_ID_CURR'] == input.customer]['AMT_ANNUITY']
    return {'income':income, 'credit':credit,'annuity': annuity}