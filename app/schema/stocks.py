import uuid
from pydantic import BaseModel, Field
from typing import Optional


class StockBase(BaseModel):
    """Base schema for Stock with common attributes"""
    ticker: str = Field(..., min_length=1, max_length=10, description="Stock ticker symbol (e.g., BBCA, BMRI)")
    name: str = Field(..., min_length=1, max_length=255, description="Full company name")
    sector: Optional[str] = Field(None, max_length=100, description="Business sector")
    current_price: Optional[float] = Field(None, gt=0, description="Current stock price")
    description: Optional[str] = Field(None, max_length=1000, description="Company description")


class StockCreate(StockBase):
    """Schema for creating a new stock"""
    pass


class StockUpdate(BaseModel):
    """Schema for updating an existing stock"""
    ticker: Optional[str] = Field(None, min_length=1, max_length=10, description="Stock ticker symbol")
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Full company name")
    sector: Optional[str] = Field(None, max_length=100, description="Business sector")
    current_price: Optional[float] = Field(None, gt=0, description="Current stock price")
    description: Optional[str] = Field(None, max_length=1000, description="Company description")


class StockResponse(StockBase):
    """Schema for stock response"""
    id: uuid.UUID = Field(..., description="Unique identifier for the stock")

    class Config:
        from_attributes = True


class StockList(BaseModel):
    """Schema for paginated stock list response"""
    stocks: list[StockResponse]
    total: int
    page: int
    page_size: int
