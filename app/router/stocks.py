from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlmodel import Session, select
from app.models.database import Stocks
from app.schema.stocks import StockCreate, StockResponse, StockUpdate, StockList
from app.models.engine import get_db
from app.models.seed_data import seed_stocks
from app.utils.pagination import paginate_query
from app.utils.stock_helpers import (
    get_stock_or_404,
    check_ticker_exists,
    normalize_ticker,
)
from typing import Optional

stocks_router = APIRouter(prefix="/stocks", tags=["Stocks"])


@stocks_router.post(
    "/", response_model=StockResponse, status_code=status.HTTP_201_CREATED
)
async def create_stock(stock: StockCreate, session: Session = Depends(get_db)):
    """Create a new stock"""
    normalized_ticker = normalize_ticker(stock.ticker)

    if check_ticker_exists(session, normalized_ticker):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stock with ticker {normalized_ticker} already exists",
        )

    stock_data = stock.model_dump()
    stock_data["ticker"] = normalized_ticker

    db_stock = Stocks(**stock_data)
    session.add(db_stock)
    session.commit()
    session.refresh(db_stock)

    return db_stock


@stocks_router.get("/", response_model=StockList)
async def get_stocks(
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    sector: Optional[str] = Query(None, description="Filter by sector"),
    session: Session = Depends(get_db),
):
    """Get paginated list of stocks"""
    query = select(Stocks)

    if sector:
        query = query.where(Stocks.sector == sector)

    # Use pagination utility (FIXES PERFORMANCE BUG - no more .all())
    result = paginate_query(session, query, page, page_size)
    stocks = [StockResponse.model_validate(s) for s in result.items]

    return StockList(
        stocks=stocks, total=result.total, page=result.page, page_size=result.page_size
    )


@stocks_router.get("/{ticker}", response_model=StockResponse)
async def get_stock(ticker: str, session: Session = Depends(get_db)):
    """Get a specific stock by ticker symbol"""
    return get_stock_or_404(session, ticker)


@stocks_router.patch("/{ticker}", response_model=StockResponse)
async def update_stock(
    ticker: str, stock_update: StockUpdate, session: Session = Depends(get_db)
):
    """Update a stock by ticker symbol"""
    stock = get_stock_or_404(session, ticker)

    update_data = stock_update.model_dump(exclude_unset=True)

    # If updating ticker, check for duplicates
    if "ticker" in update_data:
        new_ticker = normalize_ticker(update_data["ticker"])
        if new_ticker != stock.ticker and check_ticker_exists(session, new_ticker):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock with ticker {new_ticker} already exists",
            )
        update_data["ticker"] = new_ticker

    for key, value in update_data.items():
        setattr(stock, key, value)

    session.add(stock)
    session.commit()
    session.refresh(stock)

    return stock


@stocks_router.delete("/{ticker}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stock(ticker: str, session: Session = Depends(get_db)):
    """Delete a stock by ticker symbol"""
    stock = get_stock_or_404(session, ticker)
    session.delete(stock)
    session.commit()


@stocks_router.post("/seed", status_code=status.HTTP_200_OK)
async def seed_stocks_endpoint():
    """Seed database with dummy stocks (BBCA, BMRI, BBRI, BUMI)"""
    try:
        seed_stocks()
        return {"message": "Dummy stocks seeded successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error seeding stocks: {str(e)}",
        )
