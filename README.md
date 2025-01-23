# Receipt-Processor-Challenge

Hi! This is my take on the receipt-processor-challenge. I am going to build this project with FastAPI as it is a performant and light weight web framework. 

# Installation

1. Clone this repository into your directory of choice
2. Ensure that docker is installed on your native machine
3. Navigate to the root of the cloned project
4. Run this code block to build the image:

```shell
docker-compose build
```

5. Run this code block to spin it up:

```shell
docker-compose up
```

# Usage

  1. ...

# Checklist

| Feature         | Endpoint                  | Finished |
|------------------|---------------------------|----------|
| Process Receipts | `/receipts/process`       | ❌       |
| Get Points       | `/receipts/{id}/points`   | ❌       |
| BadRequest (400) |                           | ❌       |
| NotFound (404)   |                           | ❌       |

# Assumptions

  >  10 points if the time of purchase is after 2:00pm and before 4:00pm.

* Theoretically 2:00:01 pm (Hours: Minutes: Seconds) would be after 2:00pm, but as we do not include seconds in our time string, I will only distribute the 10 points if 2:01 <= purchase time <= 3:59.