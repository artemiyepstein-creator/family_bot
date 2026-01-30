from datetime import datetime, date

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, UniqueConstraint, func, Date
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Member(Base):
    __tablename__ = "members"
    __table_args__ = (
        UniqueConstraint("family_id", "telegram_id", name="uq_member_family_telegram"),
    )


    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    family_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("families.id", ondelete="CASCADE"),
        nullable=False
    )

    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    username: Mapped[str | None] = mapped_column (String (64), nullable=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)

    role: Mapped[str] = mapped_column(String(32), nullable=False, default="member")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    short_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    gender: Mapped[str | None] = mapped_column(String(16), nullable=True)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)