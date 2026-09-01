from app.infrastructure.google_ads.service import get_campaign_metrics
from app.schemas.analytics import CampaignMetricsRequest, CampaignMetricsResponse


def analyze_campaign(request: CampaignMetricsRequest) -> CampaignMetricsResponse:
    metrics = get_campaign_metrics(
        campaign_id=request.campaign_id,
        date_range=request.date_range,
    )
    return CampaignMetricsResponse(**metrics)