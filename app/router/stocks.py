from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select
from app.models.database import Stocks
from app.schema.stocks import StockCreate, StockResponse, StockUpdate, StockList
from app.models.engine import engine, get_db
from typing import Optional

stocks_router = APIRouter(prefix="/stocks", tags=["Stocks"])


def seed_dummy_stocks():
    """Seed database with dummy Indonesian stocks"""
    dummy_stocks = [
        {
            "ticker": "BBCA",
            "name": "PT Bank Central Asia Tbk",
            "sector": "Banking",
            "current_price": 9800.0,
            "description": "Largest private bank in Indonesia by market capitalization"
        },
        {
            "ticker": "BMRI",
            "name": "PT Bank Mandiri (Persero) Tbk",
            "sector": "Banking",
            "current_price": 6250.0,
            "description": "Indonesia's largest bank by assets"
        },
        {
            "ticker": "BBRI",
            "name": "PT Bank Rakyat Indonesia (Persero) Tbk",
            "sector": "Banking",
            "current_price": 5100.0,
            "description": "State-owned bank focusing on micro and small enterprises"
        },
        {
            "ticker": "BUMI",
            "name": "PT Bumi Resources Tbk",
            "sector": "Mining",
            "current_price": 142.0,
            "description": "Coal mining company operating in Kalimantan"
        }
    ]

    with Session(engine) as session:
        for stock_data in dummy_stocks:
            # Check if stock already exists
            existing = session.exec(
                select(Stocks).where(Stocks.ticker == stock_data["ticker"])
            ).first()

            if not existing:
                stock = Stocks(**stock_data)
                session.add(stock)

        session.commit()


@stocks_router.post("/", response_model=StockResponse, status_code=status.HTTP_201_CREATED)
async def create_stock(stock: StockCreate, session: Session = Depends(get_db)):
    """Create a new stock"""
    # Check if ticker already exists
    existing = session.exec(
        select(Stocks).where(Stocks.ticker == stock.ticker)
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stock with ticker {stock.ticker} already exists"
        )

    db_stock = Stocks(**stock.model_dump())
    session.add(db_stock)
    session.commit()
    session.refresh(db_stock)

    return db_stock


@stocks_router.get("/", response_model=StockList)
async def get_stocks(
    page: int = 1,
    page_size: int = 10,
    sector: Optional[str] = None,
    session: Session = Depends(get_db)
):
    """Get paginated list of stocks"""
    query = select(Stocks)

    if sector:
        query = query.where(Stocks.sector == sector)

    # Get total count
    total = len(session.exec(query).all())

    # Apply pagination
    offset = (page - 1) * page_size
    stocks_db = session.exec(query.offset(offset).limit(page_size)).all()
    stocks = [StockResponse.model_validate(stock) for stock in stocks_db]

    return StockList(
        stocks=stocks,
        total=total,
        page=page,
        page_size=page_size
    )


@stocks_router.get("/{ticker}", response_model=StockResponse)
async def get_stock(ticker: str, session: Session = Depends(get_db)):
    """Get a specific stock by ticker symbol"""
    stock = session.exec(
        select(Stocks).where(Stocks.ticker == ticker.upper())
    ).first()

    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock with ticker {ticker} not found"
        )

    return stock


@stocks_router.patch("/{ticker}", response_model=StockResponse)
async def update_stock(
    ticker: str,
    stock_update: StockUpdate,
    session: Session = Depends(get_db)
):
    """Update a stock by ticker symbol"""
    stock = session.exec(
        select(Stocks).where(Stocks.ticker == ticker.upper())
    ).first()

    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock with ticker {ticker} not found"
        )

    # Update only provided fields
    update_data = stock_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(stock, key, value)

    session.add(stock)
    session.commit()
    session.refresh(stock)

    return stock


@stocks_router.delete("/{ticker}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stock(ticker: str, session: Session = Depends(get_db)):
    """Delete a stock by ticker symbol"""
    stock = session.exec(
        select(Stocks).where(Stocks.ticker == ticker.upper())
    ).first()

    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock with ticker {ticker} not found"
        )

    session.delete(stock)
    session.commit()


@stocks_router.post("/seed", status_code=status.HTTP_200_OK)
async def seed_stocks():
    """Seed database with dummy stocks (BBCA, BMRI, BBRI, BUMI)"""
    try:
        seed_dummy_stocks()
        return {"message": "Dummy stocks seeded successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error seeding stocks: {str(e)}"
        )
