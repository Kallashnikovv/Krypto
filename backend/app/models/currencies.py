from pydantic import BaseModel
from datetime import datetime

class Forex(BaseModel):
    timestamp: datetime
    symbol: str
    price: float