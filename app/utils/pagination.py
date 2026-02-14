from pydantic import BaseModel, Field
from sqlmodel import Session, select, func
from typing import TypeVar, Generic

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="Page number (starts from 1)")
    page_size: int = Field(10, ge=1, le=100, description="Items per page")

    def calculate_offset(self) -> int:
        return (self.page - 1) * self.page_size


class PaginationResult(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int


def paginate_query(
    session: Session, query, page: int, page_size: int
) -> PaginationResult:
    """Efficient pagination with database-level counting"""
    # Use func.count() for efficient counting (fixes performance bug)
    count_query = select(func.count()).select_from(query.subquery())
    total = session.exec(count_query).one()

    # Get paginated items
    offset = (page - 1) * page_size
    items = session.exec(query.offset(offset).limit(page_size)).all()

    return PaginationResult(items=items, total=total, page=page, page_size=page_size)
