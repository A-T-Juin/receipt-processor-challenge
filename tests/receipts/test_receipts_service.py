from fastapi.testclient import TestClient
from src.receipts.main import app, volatile_memory
from src.utils.receipts_utils import score_retailer, score_total, score_items, score_purchase_date, score_purchase_time, tabulate_points

client = TestClient(app)

def test_score_retailer1():
  assert score_retailer("Target") == 6

def test_score_retailer2():
  assert score_retailer("Tar get") == 6

def test_score_retailer3():
  assert score_retailer(" Tar get") == 6

def test_score_total1():
  assert score_total("35.35") == 0

def test_score_total2():
  assert score_total("35.25") == 25

def test_score_total3():
  assert score_total("35.00") == 75

def test_score_items1():
  assert score_items([
    {
      "shortDescription": "churro",
      "price": "10.00"
    }
  ]) == 2


def test_score_items2():
  assert score_items([
    {
      "shortDescription": "churros",
      "price": "10.00"
    },
    {
      "shortDescription": "churros",
      "price": "10.00"
    }
  ]) == 5

def test_score_items3():
  assert score_items([
    {
      "shortDescription": "churros",
      "price": "10.00"
    },
    {
      "shortDescription": "churros",
      "price": "10.00"
    },
    {
      "shortDescription": "churros",
      "price": "10.00"
    }
  ]) == 5

def test_score_items4():
  assert score_items([
    {
      "shortDescription": "churro",
      "price": "10.00"
    },
    {
      "shortDescription": "churros",
      "price": "10.00"
    }
  ]) == 7

def test_score_items5():
  assert score_items([
    {
      "shortDescription": "churros",
      "price": "10.00"
    },
    {
      "shortDescription": "churros",
      "price": "10.00"
    },
    {
      "shortDescription": "churro",
      "price": "10.00"
    }
  ]) == 7

def test_score_items6():
  assert score_items([
    {
      "shortDescription": "churro",
      "price": "10.00"
    },
    {
      "shortDescription": "churro",
      "price": "10.00"
    }
  ]) == 9

def test_score_purchase_date1():
  assert score_purchase_date("10-01-01") == 6

def test_score_purchase_date2():
  assert score_purchase_date("10-01-02") == 0

def test_score_purchase_time1():
  assert score_purchase_time("14:00") == 0

def test_score_purchase_time2():
  assert score_purchase_time("14:01") == 10

def test_score_purchase_time3():
  assert score_purchase_time("15:00") == 10

def test_score_purchase_time4():
  assert score_purchase_time("16:00") == 0

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
  # this should net 12 points:
    # 6 pts for name + 6 pts for odd date
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

def test_get_points_by_receipt_id_success():
  # this works because we have only 1 item in our db from the previous test
  id = list(volatile_memory.keys())[0]
  response = client.get(f"/receipts/{id}/points")
  assert response.status_code == 200
  assert response.json() == {
    "points": 12
  }

def test_get_points_by_receipt_id_failure():
  response = client.get("/receipts/99/points")
  assert response.status_code == 404
  assert response.json() == {
    "description": "No receipt found for that ID."
  }
