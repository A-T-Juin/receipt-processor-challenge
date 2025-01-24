import typing
from pydantic import BaseModel, Field

class Item(BaseModel):
  # words, whitespace, or '-' ok
  shortDescription: str = Field(pattern=r'^[\w\s\-]+$')
  # any float with 2 trailing digits ok
  price: str = Field(pattern=r'^\d+\.\d{2}$')

class Receipt(BaseModel):
  # same as shortDescription regex but with inclusion of '&'
  retailer: str = Field(pattern=r"^[\w\s\-&]+$")
  purchaseDate: str 
  purchaseTime: str
  items: typing.List[Item]
  # same as price regex
  total: str = Field(pattern=r'^\d+\.\d{2}$')