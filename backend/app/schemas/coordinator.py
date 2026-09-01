from pydantic import BaseModel, Field, HttpUrl

from app.schemas.analytics import CampaignMetricsResponse
from app.schemas.seo import SeoAiAuditResponse


class CoordinatorReportRequest(BaseModel):
    campaign_id: str
    url: HttpUrl
    keyword: str | None = None
    date_range: str = Field(default="LAST_30_DAYS", pattern="^[A-Z0-9_]+$")


class CoordinatorReportResponse(BaseModel):
    seo: SeoAiAuditResponse
    analytics: CampaignMetricsResponse
    evaluation_phase: str
    change_policy: str
    safe_changes: list[str]
    next_actions: list[str]