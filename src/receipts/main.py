from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

volatile_memory = {
    "1000": 500, # test data
}


@app.get("/")
async def root():
    return {"message": "Hello World"}

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