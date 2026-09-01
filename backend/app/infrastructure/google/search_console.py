from datetime import date
from urllib.parse import quote

import httpx

from app.core.config import settings


async def query_search_console(
    site_url: str | None,
    start_date: date,
    end_date: date,
    row_limit: int,
) -> dict:
    access_token = settings.GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN.strip()
    configured_site = settings.GOOGLE_SEARCH_CONSOLE_SITE_URL.strip()
    site_url = site_url or configured_site
    if not access_token:
        raise ValueError("Falta GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN en backend/.env")
    if not site_url:
        raise ValueError("Indica site_url o configura GOOGLE_SEARCH_CONSOLE_SITE_URL")
    if start_date > end_date:
        raise ValueError("start_date no puede ser posterior a end_date")

    endpoint = "https://searchconsole.googleapis.com/webmasters/v3/sites/"
    encoded_site = quote(site_url, safe="")
    response = await _post_search_analytics(
        f"{endpoint}{encoded_site}/searchAnalytics/query",
        access_token,
        {
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat(),
            "dimensions": ["query"],
            "rowLimit": row_limit,
            "type": "web",
        },
    )
    rows = [
        {
            "query": row.get("keys", [""])[0],
            "clicks": round(row.get("clicks", 0)),
            "impressions": round(row.get("impressions", 0)),
            "ctr": row.get("ctr", 0),
            "position": row.get("position", 0),
        }
        for row in response.get("rows", [])
    ]
    return {
        "site_url": site_url,
        "start_date": start_date,
        "end_date": end_date,
        "rows": rows,
    }


async def _post_search_analytics(endpoint: str, token: str, payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            endpoint,
            headers={"Authorization": f"Bearer {token}"},
            json=payload,
        )
        response.raise_for_status()
        return response.json()