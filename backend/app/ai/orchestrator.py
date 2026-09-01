from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.google_ads.service import create_ad_group, create_keyword, create_search_ad
from app.schemas.automation import (
    CampaignWorkflowPreview,
    CampaignWorkflowRequest,
    CampaignWorkflowResponse,
    SeoCampaignProposalRequest,
    SeoCampaignProposalResponse,
)
from app.schemas.campaign import CampaignCreate
from app.services.campaign_service import CampaignService


async def create_campaign_workflow(
    request: CampaignWorkflowRequest,
    db: AsyncSession,
) -> CampaignWorkflowResponse:
    campaign = await CampaignService(db).create_campaign(
        CampaignCreate(
            name=request.campaign_name,
            status="PAUSED",
            budget=request.budget,
        )
    )
    campaign_id = campaign.google_campaign_id

    ad_group = create_ad_group(
        campaign_id=campaign_id,
        name=request.ad_group_name,
        cpc_bid=request.cpc_bid,
    )
    ad_group_id = ad_group["id"]

    keyword_ids = [
        create_keyword(
            ad_group_id=ad_group_id,
            text=keyword,
            match_type="PHRASE",
        )["id"]
        for keyword in request.keywords
    ]

    ad = create_search_ad(
        ad_group_id=ad_group_id,
        final_url=str(request.final_url),
        headlines=request.headlines,
        descriptions=request.descriptions,
    )

    return CampaignWorkflowResponse(
        campaign_id=campaign_id,
        ad_group_id=ad_group_id,
        keyword_ids=keyword_ids,
        ad_id=ad["id"],
    )


def preview_campaign_workflow(request: CampaignWorkflowRequest) -> CampaignWorkflowPreview:
    return CampaignWorkflowPreview(
        campaign_name=request.campaign_name,
        daily_budget=request.budget,
        ad_group_name=request.ad_group_name,
        cpc_bid=request.cpc_bid,
        keywords=request.keywords,
        final_url=request.final_url,
        headlines=request.headlines,
        descriptions=request.descriptions,
    )

async def propose_campaign_from_seo(
    request: SeoCampaignProposalRequest,
) -> SeoCampaignProposalResponse:
    from app.ai.seo_agent import audit_url_with_ai
    from app.schemas.seo import SeoAuditRequest

    seo_result = await audit_url_with_ai(
        SeoAuditRequest(url=request.url, keyword=request.keyword)
    )
    campaign_request = CampaignWorkflowRequest(
        campaign_name=request.campaign_name,
        budget=request.budget,
        ad_group_name=request.ad_group_name,
        cpc_bid=request.cpc_bid,
        keywords=seo_result.suggested_keywords,
        final_url=request.url,
        headlines=seo_result.suggested_title.split(" | ")[:3]
        + [seo_result.suggested_title],
        descriptions=[seo_result.suggested_meta_description] * 2,
    )
    return SeoCampaignProposalResponse(
        seo_audit=seo_result.model_dump(mode="json"),
        campaign=preview_campaign_workflow(campaign_request),
    )