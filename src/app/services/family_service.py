from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.family_repo import FamilyRepository

class FamilyService:
    def __init__(self, session: AsyncSession):
        self.repo = FamilyRepository(session)

    async def ensure_family_exists(self, family_id: int, title:str) -> None:
        family = await self.repo.get_by_id(family_id)
        if family is None:
            await self.repo.create(family_id=family_id, title=title)