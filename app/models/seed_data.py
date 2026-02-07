"""
Seed database with dummy stock data
"""
from sqlmodel import Session, select
from app.models.engine import engine
from app.models.database import Stocks


def seed_stocks():
    """Seed database with Indonesian dummy stocks"""
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
                print(f"✓ Added {stock_data['ticker']} - {stock_data['name']}")
            else:
                print(f"⊘ Skipped {stock_data['ticker']} - already exists")

        session.commit()
        print("\n✅ Database seeded successfully!")


if __name__ == "__main__":
    seed_stocks()
