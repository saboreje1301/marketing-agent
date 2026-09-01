from decimal import Decimal

from pydantic import BaseModel, Field, HttpUrl


class CampaignWorkflowRequest(BaseModel):
    campaign_name: str
    budget: Decimal = Field(gt=0)
    ad_group_name: str
    cpc_bid: Decimal = Field(default=Decimal("1.00"), gt=0)
    keywords: list[str] = Field(min_length=1)
    final_url: HttpUrl
    headlines: list[str] = Field(min_length=3)
    descriptions: list[str] = Field(min_length=2)


class CampaignWorkflowExecuteRequest(CampaignWorkflowRequest):
    confirm: bool = False


class CampaignWorkflowPreview(BaseModel):
    campaign_name: str
    daily_budget: Decimal
    ad_group_name: str
    cpc_bid: Decimal
    keywords: list[str]
    final_url: HttpUrl
    headlines: list[str]
    descriptions: list[str]
    requires_confirmation: bool = True


class CampaignWorkflowResponse(BaseModel):
    campaign_id: str
    ad_group_id: str
    keyword_ids: list[str]
    ad_id: str
    
class SeoCampaignProposalRequest(BaseModel):
    campaign_name: str
    ad_group_name: str
    budget: Decimal = Field(gt=0)
    cpc_bid: Decimal = Field(default=Decimal("1.00"), gt=0)
    url: HttpUrl
    keyword: str | None = None

class SeoCampaignProposalResponse(BaseModel):
    seo_audit: dict
    campaign: CampaignWorkflowPreview