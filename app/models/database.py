import uuid
from sqlmodel import SQLModel, Field
from typing import Optional

class Stocks(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    ticker: str = Field(index=True, unique=True, max_length=10, description="Stock ticker symbol (e.g., BBCA, BMRI)")
    name: str = Field(description="Full company name")
    sector: Optional[str] = Field(default=None, description="Business sector")
    current_price: Optional[float] = Field(default=None, description="Current stock price")
    description: Optional[str] = Field(default=None, description="Company description")