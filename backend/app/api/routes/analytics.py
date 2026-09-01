from fastapi import APIRouter, HTTPException
from google.ads.googleads.errors import GoogleAdsException

from app.ai.analytics_agent import analyze_campaign
from app.schemas.analytics import CampaignMetricsRequest, CampaignMetricsResponse

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics"])


@router.post("/campaign", response_model=CampaignMetricsResponse)
async def get_campaign_metrics(request: CampaignMetricsRequest):
    try:
        return analyze_campaign(request)
    except (GoogleAdsException, ValueError) as error:
        detail = str(error)
        if isinstance(error, GoogleAdsException):
            detail = "; ".join(error_detail.message for error_detail in error.failure.errors)
        raise HTTPException(status_code=400, detail=detail) from error