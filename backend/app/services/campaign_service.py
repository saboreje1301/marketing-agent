from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.google_ads.service import create_campaign as create_google_campaign
from app.models.campaign import Campaign
from app.repositories.campaign_repository import CampaignRepository
from app.schemas.campaign import CampaignCreate


class CampaignService:

    def __init__(self, db: AsyncSession):
        self.repository = CampaignRepository(db)

    async def list_campaigns(self):
        return await self.repository.get_all()

    async def create_campaign(self, data: CampaignCreate):
        google_campaign = create_google_campaign(
            name=data.name,
            status=data.status,
            budget=data.budget,
        )
        campaign = Campaign(
            google_campaign_id=google_campaign["id"],
            name=google_campaign["name"],
            status=google_campaign["status"],
            budget=google_campaign["budget"],
        )
        return await self.repository.create(campaign)