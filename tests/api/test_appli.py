import sys
import os
from fastapi.testclient import TestClient
import json
import pathlib

# Ajouter le chemin absolu du répertoire contenant l'application
api_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'api'))
sys.path.append(api_dir)

# Importer l'application FastAPI
from api_app import app

# Créer un objet TestClient
client = TestClient(app)

# Importer les données de test
data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'data_to_test.json'))
with open(data_path, 'r') as f:
    data_to_test = json.load(f)

def test_read_main():
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

# import features to be tested
with open(api_dir/'../data/data_to_test.json', 'r') as f:
    data_to_be_tested = json.load(f)

def test_exp_score():
    response = client.post('/prediction', json=data_to_be_tested)

    assert response.status_code == 200