from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .base import Base
    from .user import User

from enum import Enum

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

class Role(Enum):
    Worker = 0
    Admin = 1
    Owner = 2


class Team(Base):
    __tablename__ = "Teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    name: Mapped[str] = mapped_column(unique=True) 

    # admins: Mapped[list["User"]] = relationship(back_populates="team_member") # ???
    # members: Mapped[list["TeamMembers"]] = relationship(back_populates="team")


class TeamMembers(Base):
    __tablename__ = "TeamMembers"

    member_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    role: Mapped[Role] = mapped_column()

    # team_: Mapped["Team"] = relationship(back_populates="members")
    # user: Mapped["User"] = relationship(back_populates="teams")