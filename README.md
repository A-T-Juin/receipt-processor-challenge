# Receipt-Processor-Challenge

Hi! This is my take on the receipt-processor-challenge. I am going to build this project with FastAPI as it is a performant and light weight web framework. 

# Installation

1. Clone this repository into your directory of choice
2. Ensure that docker is installed on your machine
3. Start docker
4. Navigate to the root of the cloned project
5. Run this code block to build the image:

```shell
docker-compose build
```

6. Run this code block to spin it up:

```shell
docker-compose up
```

# Usage

| Routes                            | description |
|-----------------------------------|-------------|
| `localhost:80/receipts/process`    | Accepts ```POST``` method and calculate points earned for a valid receipt. Returns in the form ```{id: str}``` |
| `localhost:80/receipts/{id}/points`| Accepts ```GET``` method and returns the number of points earned by the receipt with the associated receiptID. Returns in the form ```{points: int}``` |


We can now interact with the receipt-processor at the provided Routes using curl or api tool like postman.

# Checklist

| Feature         | Endpoint                  | Finished |
|------------------|---------------------------|----------|
| Process Receipts | `/receipts/process`       | ✅       |
| Get Points       | `/receipts/{id}/points`   | ✅       |
| BadRequest (400) |                           | ✅       |
| NotFound (404)   |                           | ✅       |

# Assumptions

  >  10 points if the time of purchase is after 2:00pm and before 4:00pm.

* Theoretically 2:00:01 pm (Hours: Minutes: Seconds) would be after 2:00pm, but as we do not include seconds in our time string, I will only distribute the 10 points if 2:01 <= purchase time <= 3:59 or (14:01 <= purchase time <= 15:59).

# Extra

* I used the provided regex patterns to validate specific parts of the schema and conducted a few basic tests for the following fields. These tests are limited in scope and not exhaustive.
  * retailer
  * total
  * shortDescription
  * price