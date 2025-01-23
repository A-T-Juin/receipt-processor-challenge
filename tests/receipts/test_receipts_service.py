from fastapi.testclient import TestClient

from src.receipts.main import app

client = TestClient(app)

def test_root():
  response = client.get("/")
  assert response.status_code == 200
  assert response.json() == {
    "message": "Hello World"
  }

def test_get_points_by_receipt_id_success():
  response = client.get("/receipts/1000/points")
  assert response.status_code == 200
  assert response.json() == {
    "points": 500
  }

def test_get_points_by_receipt_id_failure():
  response = client.get("/receipts/99/points")
  assert response.status_code == 404
  assert response.json() == {
    "description": "No receipt found for that ID."
  }