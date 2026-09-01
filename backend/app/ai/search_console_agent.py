from app.infrastructure.google.search_console import query_search_console
from app.schemas.search_console import SearchConsoleRequest, SearchConsoleResponse


async def analyze_search_console(request: SearchConsoleRequest) -> SearchConsoleResponse:
    result = await query_search_console(
        site_url=str(request.site_url) if request.site_url else None,
        start_date=request.start_date,
        end_date=request.end_date,
        row_limit=request.row_limit,
    )
    return SearchConsoleResponse(**result)