from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.member_repo import MemberRepository

class MemberService:
    def __init__(self, session: AsyncSession):
        self.repo = MemberRepository(session)
    
    async def ensure_member_exists(
        self,
        family_id: int,
        telegram_id: int,
        full_name: str,
        username: str | None,
        role: str = "member"
    ) -> None:
        existing = await self.repo.get_by_family_and_telegram(family_id, telegram_id)
        if existing is not None:
            return existing.role
        
        member_count = await self.repo.count_by_family(family_id)
        role = "owner" if member_count == 0 else "member"

        await self.repo.create(
            family_id=family_id,
            telegram_id=telegram_id,
            full_name=full_name,
            username=username,
            role=role,
        )
        return role