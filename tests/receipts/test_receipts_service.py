from fastapi.testclient import TestClient
from src.receipts.main import app
from src.utils.receipts_utils import tabulate_points

client = TestClient(app)

def test_get_points_by_receipt_id_success():
  response = client.get("/receipts/63cf49ec-8097-49d1-85a0-21c24176fcaa/points")
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

def test_tabulate_points():
  target_example = {
    "retailer": "Target",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
      {
        "shortDescription": "Mountain Dew 12PK",
        "price": "6.49"
      },{
        "shortDescription": "Emils Cheese Pizza",
        "price": "12.25"
      },{
        "shortDescription": "Knorr Creamy Chicken",
        "price": "1.26"
      },{
        "shortDescription": "Doritos Nacho Cheese",
        "price": "3.35"
      },{
        "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
        "price": "12.00"
      }
    ],
    "total": "35.35"
  }

  m_and_m_example = {
    "retailer": "M&M Corner Market",
    "purchaseDate": "2022-03-20",
    "purchaseTime": "14:33",
    "items": [
      {
        "shortDescription": "Gatorade",
        "price": "2.25"
      },{
        "shortDescription": "Gatorade",
        "price": "2.25"
      },{
        "shortDescription": "Gatorade",
        "price": "2.25"
      },{
        "shortDescription": "Gatorade",
        "price": "2.25"
      }
    ],
    "total": "9.00"
  }

  assert tabulate_points(target_example) == 28
  assert tabulate_points(m_and_m_example) == 109

def test_process_receipt_validation_shortDescrption():
  response = client.post(
    "/receipts/process",
    json={
      "retailer": "Target",
      "purchaseDate": "2022-01-01",
      "purchaseTime": "13:01",
      "items": [
        {
          "shortDescription": "Mountain & Dew 12PK",
          "price": "6.49"
        }
      ],
      "total": "35.35"
    }
  )
  assert response.status_code == 400

def test_process_receipt_validation_price():
  response = client.post(
    "/receipts/process",
    json={
      "retailer": "Target!",
      "purchaseDate": "2022-01-01",
      "purchaseTime": "13:01",
      "items": [
        {
          "shortDescription": "Mountain Dew 12PK",
          "price": "6.9"
        }
      ],
      "total": "35.35"
    }
  )
  assert response.status_code == 400

def test_process_receipt_validation_total():
  response = client.post(
    "/receipts/process",
    json={
      "retailer": "Target!",
      "purchaseDate": "2022-01-01",
      "purchaseTime": "13:01",
      "items": [
        {
          "shortDescription": "Mountain Dew 12PK",
          "price": "6.49"
        }
      ],
      "total": "35"
    }
  )
  assert response.status_code == 400

def test_process_receipt_validation_retailer():
  response = client.post(
    "/receipts/process",
    json={
      "retailer": "Target!",
      "purchaseDate": "2022-01-01",
      "purchaseTime": "13:01",
      "items": [
        {
          "shortDescription": "Mountain Dew 12PK",
          "price": "6.49"
        }
      ],
      "total": "35.35"
    }
  )
  assert response.status_code == 400

def test_process_receipt_success():
  response = client.post(
    "/receipts/process",
    json={
      "retailer": "Target",
      "purchaseDate": "2022-01-01",
      "purchaseTime": "13:01",
      "items": [
        {
          "shortDescription": "Mountain Dew 12PK",
          "price": "6.49"
        }
      ],
      "total": "35.35"
    }
  )
  parsed_response = response.json()
  assert response.status_code == 200
  assert type(parsed_response["id"])  == str
  

def test_process_receipt_failure():
  response = client.post(
    "/receipts/process",
    json={
      "retailer": "Target",
      "purchaseDate": "2022-01-01",
      "purchaseTime": "13:01",
      "items": [
        {
          "shortDescription": "Mountain Dew 12PK",
          "price": "6.49"
        }
      ]
    }
  )

  assert response.status_code == 400
  assert response.json() == {
    "description": "The receipt is invalid."
  }
