from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.automation import router as automation_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes.campaigns import router as campaign_router
from app.api.routes.coordinator import router as coordinator_router
from app.api.routes.seo import router as seo_router
from app.api.routes.search_console import router as search_console_router
from app.core.config import settings

app = FastAPI(
    title="Marketing AI",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost", "127.0.0.1", "http://localhost:3000", "http://localhost:8080"] if settings.DEBUG else ["https://tudominio.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(campaign_router)
app.include_router(automation_router)
app.include_router(seo_router)
app.include_router(analytics_router)
app.include_router(coordinator_router)
app.include_router(search_console_router)