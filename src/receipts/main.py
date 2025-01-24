from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.receipts.schemas import Receipt
from src.utils.receipts_utils import tabulate_points

app = FastAPI()

volatile_memory = {
    "1000": 500, # test data
}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/receipts/process")
def process_receipt(receipt: Receipt):
    parsed_receipt_input = Receipt.model_dump(receipt)
    new_id = str(len(volatile_memory))
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