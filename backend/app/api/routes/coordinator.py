import httpx
from fastapi import APIRouter, HTTPException
from google.ads.googleads.errors import GoogleAdsException

from app.ai.coordinator_agent import create_report
from app.schemas.coordinator import CoordinatorReportRequest, CoordinatorReportResponse

router = APIRouter(prefix="/api/v1/coordinator", tags=["Coordinator"])


@router.post("/report", response_model=CoordinatorReportResponse)
async def get_coordinator_report(request: CoordinatorReportRequest):
    try:
        return await create_report(request)
    except (GoogleAdsException, ValueError, OSError, httpx.HTTPError, KeyError) as error:
        detail = str(error)
        if isinstance(error, GoogleAdsException):
            detail = "; ".join(error_detail.message for error_detail in error.failure.errors)
        raise HTTPException(status_code=400, detail=detail) from error