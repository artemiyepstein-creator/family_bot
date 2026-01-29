from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.shopping import ShoppingItem


class ShoppingRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_item(self, family_id: int, created_by: int, title: str) -> ShoppingItem:
        item = ShoppingItem(family_id=family_id, created_by=created_by, title=title)
        self.session.add(item)
        await self.session.commit()
        return item
    
    async def list_open(self, family_id: int, limit: int = 50) -> list[ShoppingItem]:
        stmt = (
            select(ShoppingItem).where(ShoppingItem.family_id==family_id, ShoppingItem.is_done==False).order_by(ShoppingItem.created_at.asc()).limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
    
    async def set_done(self, family_id: int, item_id: int, done: bool) -> bool:
        stmt = (
            update(ShoppingItem)
            .where(ShoppingItem.family_id == family_id, ShoppingItem.id == item_id)
            .values(is_done=done)
        )
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.rowcount > 0
    
    async def delete_item(self, family_id: int, item_id: int) -> bool:
        stmt = delete(ShoppingItem).where(
            ShoppingItem.family_id == family_id,
            ShoppingItem.id == item_id,
        )
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.rowcount > 0