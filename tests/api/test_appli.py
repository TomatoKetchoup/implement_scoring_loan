import os
import sys
import json
from fastapi.testclient import TestClient

# Ajouter le chemin relatif du répertoire contenant l'application
api_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../api'))
sys.path.append(api_dir)

# Importer l'application FastAPI
from api_app import app

# Créer un objet TestClient
client = TestClient(app)

# Data to test
data_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/data_to_test.json'))
with open(data_file, 'r') as f:
    data_to_test = json.load(f)

def test_read_main():
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

def test_api_prediction():
    response = client.post('/prediction', json=data_to_test)
    assert response.status_code == 200
    assert 'predict_proba' in response.json()
