import numpy as np
from fastapi import FastAPI
import pickle
import joblib
from pydantic import BaseModel

app = FastAPI()


with open('explainer.pkl', 'rb') as f:
    explainer = pickle.load(f)
model_saved = joblib.load('scoring_loan.joblib')
pipeline_selecting_feature =  model_saved.named_steps['feature_selection']
class UserInput(BaseModel):
    features_dict: dict
@app.post("/prediction")
async def recevoir_dictionnaire(features: dict):
    vget = np.vectorize(features.get)
    # Use the vectorized get method to select values from the dictionary
    instance = vget(pipeline_selecting_feature.get_feature_names_out())

    exp = explainer.explain_instance(instance, model_saved
                                     .set_params(feature_selection=None)
                                     .predict_proba, num_features=5)

    ## Probabilites Class 0 and Class 1
    explainer_proba = exp.predict_proba.tolist()
    ## fiabilite model
    model_reliability = exp.score
    #Feature importance
    feature_importance = [t[1] for t in exp.as_map()[1]]
    selected_indices = [t[0] for t in exp.as_map()[1]]
    feature_names = pipeline_selecting_feature.get_feature_names_out()[selected_indices].tolist()
    return { 'predict_proba':explainer_proba, 'model reliability': model_reliability,
             'importance':feature_importance, 'feature_names':feature_names}


