from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.campaign import Campaign


class CampaignRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(
            select(Campaign)
        )
        return result.scalars().all()

    async def create(self, campaign: Campaign):
        self.db.add(campaign)
        await self.db.commit()
        await self.db.refresh(campaign)
        return campaign