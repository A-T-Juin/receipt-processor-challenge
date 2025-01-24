import math

def score_retailer(retailer_name):
  score = 0
  for char in retailer_name:
    if char.isalnum(): # only gets points for alphanumeric value
      score += 1
  return score

def score_total(receipt_total):
  score = 0
  cent_amount = receipt_total[-2:]
  if cent_amount == "00":
    score += 75 # we add 75 because it is a round dollar amount and is a multiple of .25
  else:
    if int(cent_amount) % 25 == 0:
      score += 25
  return score

def score_items(items):
  num_items = len(items)
  score = 5 * (num_items // 2)
  for item in items:
    description = item["shortDescription"]
    price = item["price"]
    trimmed_description = description.strip()
    if len(trimmed_description) % 3 == 0:
      score += math.ceil(float(price) * .2)
  return score
  
def score_purchase_date(purchase_date):
  # date is given as yyyy-mm-dd
  score = 0
  date = purchase_date[-2:]
  if int(date) & 1: # check odd using binary
    score = 6
  return score 

def score_purchase_time(purchase_time):
  # time is given as hh:mm
  # because we are using a 24 hour clock, 2:00pm and 4:00pm will be
  # 14:00 and 15:59 respectively
  score = 0
  hour_of_time = int(purchase_time[:2])
  minute_of_time = int(purchase_time[-2:])
  if 14 <= hour_of_time <= 15 and 1 <= minute_of_time <= 59:
    score = 10
  return score

# the conditions and methods we calculate points
score_methods = {
  "retailer": score_retailer,
  "total": score_total,
  "items": score_items,
  "purchaseDate": score_purchase_date,
  "purchaseTime": score_purchase_time
}

def tabulate_points(receipt):
  total = 0
  for key, value in receipt.items():
    # go through the entire receipt adding points for each passing
    # condition.
    total += score_methods[key](value)
      
  return total
