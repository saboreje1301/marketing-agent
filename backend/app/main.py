from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.optimization import router as optimization_router
from app.core.config import settings

app = FastAPI(
    title="Marketing AI - Conversion Optimizer",
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

@app.get("/", tags=["root"])
async def root():
    return {"status": "ok", "service": "Marketing AI - Conversion Optimizer", "version": "0.1.0"}

app.include_router(optimization_router)