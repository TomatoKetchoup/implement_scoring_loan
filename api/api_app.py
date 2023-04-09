from fastapi import FastAPI
import pickle
import pandas as pd
import pathlib
import sys
import dill
from typing import Dict
import numpy as np


app = FastAPI()

# api_dir = pathlib.Path(__file__).resolve().parent
# sys.path.append(str(api_dir))

# Simple unit test
@app.get("/test")
async def read_main():
    return {"msg": "Hello World"}

### End simple test
with open(('explainer.pkl'), 'rb') as f:
    explainer = pickle.load(f)
with open(("pipe_prod.dill"), "rb") as f:
    pipe_prod = dill.load(f)
with open(("preprocessor.pkl"), "rb") as f:
    preprocessor = pickle.load(f)

# with open(api_dir.joinpath('explainer.pkl'), 'rb') as f:
#     explainer = pickle.load(f)
# with open(api_dir.joinpath("pipe_prod.dill"), "rb") as f:
#     pipe_prod = dill.load(f)
# with open(api_dir.joinpath("preprocessor.pkl"), "rb") as f:
#     preprocessor = pickle.load(f)

@app.post("/prediction")
async def recevoir_dictionnaire(features : Dict):
        df = pd.DataFrame.from_dict(features, orient='index', columns=['valeur']).T
        df = df.replace('missing', np.nan)
        nparray = preprocessor.transform(df)
        #
        exp = explainer.explain_instance(nparray.flatten(),
                                     pipe_prod.named_steps['model'].predict_proba,
                                     num_features=16)

    ## Probabilites Class 0 and Class 1
        explainer_proba = exp.predict_proba.tolist()

        #Feature importance
        feature_importance = [t[1] for t in exp.as_map()[1]]
        selected_indices = [t[0] for t in exp.as_map()[1]]
        feature_names = (pipe_prod.named_steps['cleaning'].named_steps['selector'].get_feature_names_out()[selected_indices]).tolist()
        return { 'predict_proba':explainer_proba,'importance':feature_importance, 'feature_names':feature_names}

