from api.api_app import read_main
import json
import pathlib
from fastapi.testclient import TestClient
api_dir = pathlib.Path(__file__).parent.resolve()
print(api_dir)

client = TestClient(read_main)
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