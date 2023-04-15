from fastapi import FastAPI
import pickle
import pandas as pd
import pathlib
import sys
import joblib
from typing import Dict
import numpy as np

api_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(api_dir))
app = FastAPI()
# Simple unit test
@app.get("/test")
async def read_main():
    return {"msg": "Hello World"}
### End simple test

## Import
with open(api_dir.joinpath(('explainer.pkl')), 'rb') as f:
    explainer = pickle.load(f)

pipe_prod = joblib.load(api_dir.joinpath('scoring_loan.joblib'))

with open(api_dir.joinpath(("preprocessor.pkl")), "rb") as f:
    preprocessor = pickle.load(f)

@app.post("/prediction")
async def recevoir_dictionnaire(features : Dict):
        df = pd.DataFrame.from_dict(features, orient='index', columns=['valeur']).T
        df = df.replace('missing', np.nan)
        nparray = preprocessor.transform(df)
        ### Explainer
        exp = explainer.explain_instance(nparray.flatten(),
                                     pipe_prod.named_steps['model'].predict_proba,
                                     num_features=16)

        ## Probabilites Class 0 and Class 1
        explainer_proba = exp.predict_proba.tolist()

        #Feature importance
        feature_importance = [t[1] for t in exp.as_map()[1]]
        selected_indices = [t[0] for t in exp.as_map()[1]]
        feature_names = pipe_prod.named_steps['preprocessor'].get_feature_names_out()[selected_indices].tolist()

        return { 'predict_proba':explainer_proba,'importance':feature_importance, 'feature_names':feature_names}

