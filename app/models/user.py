from .base import Base
from .team import TeamMembers

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(primary_key=True)
    
    hashed_password: Mapped[str] = mapped_column()
    salt: Mapped[str] = mapped_column()

    surename: Mapped[str | None] = mapped_column(nullable=True)

    teams: Mapped[list["TeamMembers"]] = relationship(back_populates="") # ??