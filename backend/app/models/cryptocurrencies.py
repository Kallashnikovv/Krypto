from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

#Data Models
class CryptoRate(BaseModel):
    id: int
    name: str
    symbol: str
    price_usd: float
    percent_change_1h: Optional[float] = None
    percent_change_24h: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.now)
