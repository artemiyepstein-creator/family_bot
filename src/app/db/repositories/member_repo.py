from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.member import Member

class MemberRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_family_and_telegram(self, family_id: int, telegram_id: int) -> Member | None:
        stmt = select(Member).where(
            Member.family_id == family_id,
            Member.telegram_id == telegram_id,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def create(
            self,
            family_id: int,
            telegram_id: int,
            full_name: str,
            username: str | None,
            role: str = "member"
    ) -> Member:
        member = Member(
            family_id=family_id,
            telegram_id=telegram_id,
            full_name=full_name,
            username=username,
            role=role,

        )
        self.session.add(member)
        await self.session.commit()
        return member
    
    async def count_by_family(self, family_id:int) -> int:
        stmt = select(func.count()).select_from(Member).where(Member.family_id == family_id)
        result = await self.session.execute(stmt)
        return int(result.scalar_one())