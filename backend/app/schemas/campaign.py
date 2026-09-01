from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CampaignCreate(BaseModel):
    google_campaign_id: str | None = None
    name: str
    status: str
    budget: Decimal = Decimal("0.00")


class CampaignResponse(BaseModel):
    id: int
    google_campaign_id: str
    name: str
    status: str
    budget: Decimal

    model_config = ConfigDict(from_attributes=True)


class AdGroupCreate(BaseModel):
    name: str
    cpc_bid: Decimal = Decimal("1.00")


class AdGroupResponse(BaseModel):
    id: str
    name: str
    status: str
    campaign_id: str


class KeywordCreate(BaseModel):
    text: str
    match_type: str = "BROAD"


class KeywordResponse(BaseModel):
    id: str
    text: str
    match_type: str
    status: str
    ad_group_id: str


class SearchAdCreate(BaseModel):
    final_url: str
    headlines: list[str]
    descriptions: list[str]


class SearchAdResponse(BaseModel):
    id: str
    ad_group_id: str
    status: str
    final_url: str