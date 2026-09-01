import httpx
from fastapi import APIRouter, Depends, HTTPException
from google.ads.googleads.errors import GoogleAdsException
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.orchestrator import (
    create_campaign_workflow,
    preview_campaign_workflow,
    propose_campaign_from_seo,
)
from app.database.database import get_db
from app.schemas.automation import (
    CampaignWorkflowExecuteRequest,
    CampaignWorkflowPreview,
    CampaignWorkflowResponse,
    CampaignWorkflowRequest,
    SeoCampaignProposalRequest,
    SeoCampaignProposalResponse,
)

router = APIRouter(
    prefix="/api/v1/automation",
    tags=["Automation"],
)


@router.post("/campaigns", response_model=CampaignWorkflowResponse)
async def run_campaign_workflow(
    request: CampaignWorkflowExecuteRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        if not request.confirm:
            raise HTTPException(
                status_code=409,
                detail="Confirma la creación enviando confirm=true después de revisar el resumen.",
            )
        return await create_campaign_workflow(request, db)
    except (GoogleAdsException, ValueError) as error:
        detail = str(error)
        if isinstance(error, GoogleAdsException):
            detail = "; ".join(error_detail.message for error_detail in error.failure.errors)
        raise HTTPException(status_code=400, detail=detail) from error


@router.post("/campaigns/preview", response_model=CampaignWorkflowPreview)
async def preview_campaign(request: CampaignWorkflowRequest):
    return preview_campaign_workflow(request)


@router.post("/seo-campaign/preview", response_model=SeoCampaignProposalResponse)
async def preview_seo_campaign(request: SeoCampaignProposalRequest):
    try:
        return await propose_campaign_from_seo(request)
    except (ValueError, OSError, httpx.HTTPError, KeyError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error