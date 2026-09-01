import httpx
from fastapi import APIRouter, HTTPException

from app.ai.search_console_agent import analyze_search_console
from app.schemas.search_console import SearchConsoleRequest, SearchConsoleResponse

router = APIRouter(prefix="/api/v1/search-console", tags=["Search Console"])


@router.post("/queries", response_model=SearchConsoleResponse)
async def get_search_console_queries(request: SearchConsoleRequest):
    try:
        return await analyze_search_console(request)
    except (ValueError, OSError, httpx.HTTPError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error