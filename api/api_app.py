import pandas as pd
from fastapi import FastAPI
import pickle
import joblib
import numpy as np
from fastapi.responses import JSONResponse

with open('C:/Users/td/implement_scoring_loan/api/explainer.pkl', 'rb') as f:
    explainer = pickle.load(f)

model_saved = joblib.load('C:/Users/td/implement_scoring_loan/api/scoring_loan.joblib')

with open('C:/Users/td/implement_scoring_loan/dashboard/selected_feature_names.pkl', 'rb') as f:
    selected_feature_names = pickle.load(f)

app = FastAPI()

@app.post("/local_importance")
def process_data():
    data_customer = np.array([0.00000000e+00, -9.46100000e+03, -6.37000000e+02, 8.30369674e-02,
                              2.62948593e-01, 1.39375780e-01, 0.00000000e+00, 0.00000000e+00,
                              -1.43700000e+03, -8.74000000e+02, -4.99875000e+02, 2.50000000e-01,
                              7.50000000e-01, 1.00000000e+00, 0.00000000e+00, 1.00000000e+00])
    exp = explainer.explain_instance(data_customer, model_saved.set_params(selector=None).predict_proba, num_features=5, num_samples=5)
    return JSONResponse(content={"result": exp.as_html()})
