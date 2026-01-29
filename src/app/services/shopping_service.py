from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.shopping_repo import ShoppingRepository


class ShoppingService:
    def __init__(self, session: AsyncSession):
        self.repo = ShoppingRepository(session)

    async def add(self, family_id: int, user_id: int, title: str):
        title = title.strip()
        if not title:
            raise ValueError("empty_title")
        return await self.repo.add_item(family_id=family_id, created_by=user_id, title=title)

    async def list_open(self, family_id: int):
        return await self.repo.list_open(family_id=family_id)

    async def done(self, family_id: int, item_id: int):
        return await self.repo.set_done(family_id=family_id, item_id=item_id, done=True)

    async def undone(self, family_id: int, item_id: int):
        return await self.repo.set_done(family_id=family_id, item_id=item_id, done=False)

    async def delete(self, family_id: int, item_id: int):
        return await self.repo.delete_item(family_id=family_id, item_id=item_id)