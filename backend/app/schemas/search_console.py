from datetime import date

from pydantic import BaseModel, Field, HttpUrl


class SearchConsoleRequest(BaseModel):
    site_url: HttpUrl | None = None
    start_date: date
    end_date: date
    row_limit: int = Field(default=25, ge=1, le=25000)


class SearchConsoleRow(BaseModel):
    query: str
    clicks: int
    impressions: int
    ctr: float
    position: float


class SearchConsoleResponse(BaseModel):
    site_url: str
    start_date: date
    end_date: date
    rows: list[SearchConsoleRow]