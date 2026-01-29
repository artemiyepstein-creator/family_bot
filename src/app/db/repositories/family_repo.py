from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.family import Family

class FamilyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, family_id: int) -> Family | None:
        stmt = select(Family).where(Family.id == family_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def create(self, family_id: int, title: str) -> Family:
        family = Family(id=family_id, title=title)
        self.session.add(family)
        await self.session.commit()
        return family