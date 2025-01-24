import typing
from pydantic import BaseModel

class Item(BaseModel):
  shortDescription: str
  price: str

class Receipt(BaseModel):
  retailer: str
  purchaseDate: str
  purchaseTime: str
  items: typing.List[Item]
  total: str