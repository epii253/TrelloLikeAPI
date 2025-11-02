from .base import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .team import TeamMembers

from sqlalchemy import ForeignKey, Integer
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

class User(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    hashed_password: Mapped[str] = mapped_column()
    salt: Mapped[str] = mapped_column()

    surename: Mapped[Optional[str]] = mapped_column()

    #teams: Mapped[list["TeamMembers"]] = relationship(back_populates="user") # ??