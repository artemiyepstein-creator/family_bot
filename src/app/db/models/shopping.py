from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class ShoppingItem(Base):
    __tablename__="shoping_item"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    family_id: Mapped[int] = mapped_column(
        BigInteger, 
        ForeignKey("families.id", ondelete="CASCADE"),
        nullable=False,
        )
    
    created_by: Mapped[int] = mapped_column(BigInteger, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)

    is_done: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )