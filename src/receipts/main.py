import uuid
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.receipts.schemas import Receipt
from src.utils.receipts_utils import tabulate_points

app = FastAPI()

volatile_memory = {
    "63cf49ec-8097-49d1-85a0-21c24176fcaa": 500, # test data
}

# overrides FastAPI's default validation error to match design specifications
@app.exception_handler(RequestValidationError)
async def receipt_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"description": "The receipt is invalid."}
    )

@app.post("/receipts/process")
def process_receipt(receipt: Receipt):
    parsed_receipt_input = Receipt.model_dump(receipt)
    new_id = str(uuid.uuid4())
    points_earned = tabulate_points(parsed_receipt_input)
    volatile_memory[new_id] = points_earned
    return {"id": new_id}

# grab points from our db
@app.get("/receipts/{receipt_id}/points")
async def get_points_by_receipt_id(receipt_id: str):
    # receipt_id found
    if receipt_id in volatile_memory:
        return {"points": volatile_memory[receipt_id]}
    # receipt_id not found
    else:
        return JSONResponse(
            status_code=404,
            content={"description": "No receipt found for that ID."}
        )