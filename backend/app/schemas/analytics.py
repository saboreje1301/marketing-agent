from decimal import Decimal

from pydantic import BaseModel, Field


class CampaignMetricsRequest(BaseModel):
    campaign_id: str
    date_range: str = Field(default="LAST_30_DAYS", pattern="^[A-Z0-9_]+$")


class CampaignMetricsResponse(BaseModel):
    campaign_id: str
    date_range: str
    impressions: int
    clicks: int
    ctr: Decimal
    cost: Decimal
    conversions: Decimal
    average_cpc: Decimal