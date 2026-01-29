from sqlalchemy import BigInteger, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.db.base import Base

class Family(Base):
    __tablename__="families"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title:Mapped[str] = mapped_column(String(255), nullable=False, default="")
    created_at: Mapped[datetime]=mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False
        )