from fastapi import APIRouter, HTTPException
import httpx

from app.ai.seo_agent import audit_url, audit_url_with_ai
from app.schemas.seo import SeoAiAuditResponse, SeoAuditRequest, SeoAuditResponse

router = APIRouter(prefix="/api/v1/seo", tags=["SEO"])


@router.post("/audit", response_model=SeoAuditResponse)
async def run_seo_audit(request: SeoAuditRequest):
    try:
        return await audit_url(request)
    except (ValueError, OSError, httpx.HTTPError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/ai-audit", response_model=SeoAiAuditResponse)
async def run_ai_seo_audit(request: SeoAuditRequest):
    try:
        return await audit_url_with_ai(request)
    except (ValueError, OSError, httpx.HTTPError, KeyError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error