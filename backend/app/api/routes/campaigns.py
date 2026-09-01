from fastapi import APIRouter, Depends, HTTPException
from google.ads.googleads.errors import GoogleAdsException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.infrastructure.google_ads.service import list_campaigns as list_google_campaigns
from app.infrastructure.google_ads.service import (
    create_ad_group,
    create_keyword,
    create_search_ad,
    list_ad_groups,
)
from app.schemas.campaign import (
    AdGroupCreate,
    AdGroupResponse,
    CampaignCreate,
    CampaignResponse,
    KeywordCreate,
    KeywordResponse,
    SearchAdCreate,
    SearchAdResponse,
)
from app.services.campaign_service import CampaignService

router = APIRouter(
    prefix="/api/v1/campaigns",
    tags=["Campaigns"],
)


@router.get("", response_model=list[CampaignResponse])
async def get_campaigns(
    db: AsyncSession = Depends(get_db),
):
    service = CampaignService(db)
    return await service.list_campaigns()


@router.post("", response_model=CampaignResponse)
async def create_campaign(
    campaign: CampaignCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        service = CampaignService(db)
        return await service.create_campaign(campaign)
    except (GoogleAdsException, ValueError) as error:
        detail = str(error)
        if isinstance(error, GoogleAdsException):
            messages = []
            for error_detail in error.failure.errors:
                field_path = ""
                if error_detail.location:
                    field_path = " (campo: " + " > ".join(
                        element.field_name
                        for element in error_detail.location.field_path_elements
                    ) + ")"
                messages.append(f"{error_detail.message}{field_path}")
            detail = "; ".join(messages) or str(error)
        raise HTTPException(status_code=400, detail=detail) from error


@router.get("/google-ads")
async def get_google_ads_campaigns():
    try:
        return await _list_google_campaigns()
    except ValueError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error


@router.post("/{google_campaign_id}/ad-groups", response_model=AdGroupResponse)
async def create_campaign_ad_group(
    google_campaign_id: str,
    ad_group: AdGroupCreate,
):
    try:
        return create_ad_group(
            campaign_id=google_campaign_id,
            name=ad_group.name,
            cpc_bid=ad_group.cpc_bid,
        )
    except (GoogleAdsException, ValueError) as error:
        detail = str(error)
        if isinstance(error, GoogleAdsException):
            detail = "; ".join(error_detail.message for error_detail in error.failure.errors)
        raise HTTPException(status_code=400, detail=detail) from error


@router.get("/{google_campaign_id}/ad-groups", response_model=list[AdGroupResponse])
async def get_campaign_ad_groups(google_campaign_id: str):
    try:
        return list_ad_groups(google_campaign_id)
    except (GoogleAdsException, ValueError) as error:
        detail = str(error)
        if isinstance(error, GoogleAdsException):
            detail = "; ".join(error_detail.message for error_detail in error.failure.errors)
        raise HTTPException(status_code=400, detail=detail) from error


@router.post("/ad-groups/{ad_group_id}/keywords", response_model=KeywordResponse)
async def create_ad_group_keyword(
    ad_group_id: str,
    keyword: KeywordCreate,
):
    try:
        return create_keyword(
            ad_group_id=ad_group_id,
            text=keyword.text,
            match_type=keyword.match_type,
        )
    except (GoogleAdsException, ValueError) as error:
        detail = str(error)
        if isinstance(error, GoogleAdsException):
            detail = "; ".join(error_detail.message for error_detail in error.failure.errors)
        raise HTTPException(status_code=400, detail=detail) from error


@router.post("/ad-groups/{ad_group_id}/ads", response_model=SearchAdResponse)
async def create_ad_group_search_ad(
    ad_group_id: str,
    ad: SearchAdCreate,
):
    try:
        return create_search_ad(
            ad_group_id=ad_group_id,
            final_url=ad.final_url,
            headlines=ad.headlines,
            descriptions=ad.descriptions,
        )
    except (GoogleAdsException, ValueError) as error:
        detail = str(error)
        if isinstance(error, GoogleAdsException):
            detail = "; ".join(error_detail.message for error_detail in error.failure.errors)
        raise HTTPException(status_code=400, detail=detail) from error


async def _list_google_campaigns():
    return list_google_campaigns()