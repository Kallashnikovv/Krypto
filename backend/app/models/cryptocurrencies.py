from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

#Data Models
class CryptoRate(BaseModel):
    id: int
    symbol: str
    name: str
    price: float
    percentage: Optional[float] = None