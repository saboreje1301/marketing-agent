from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.database.database import get_db

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
async def health():
    """Verificar estado general de la app"""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "debug": settings.DEBUG,
    }


@router.get("/db")
async def db_health(
    db: AsyncSession = Depends(get_db),
):
    """Verificar conexión a PostgreSQL"""
    try:
        await db.execute(text("SELECT 1"))
        return {"database": "connected"}
    except Exception as e:
        return {"database": "error", "detail": str(e)}, 503


@router.get("/integrations")
async def integrations_health():
    """Verificar estado de integraciones externas"""
    integrations = {
        "google_ads": bool(settings.GOOGLE_ADS_DEVELOPER_TOKEN),
        "google_search_console": bool(settings.GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN),
        "gemini": bool(settings.GEMINI_API_KEY),
    }
    all_configured = all(integrations.values())
    return {
        "integrations": integrations,
        "status": "configured" if all_configured else "partial",
    }

