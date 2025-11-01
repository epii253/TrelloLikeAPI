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
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    name: Mapped[str] = mapped_column() 

    admins: Mapped[list["User"]] = relationship(back_populates="team")
    members: Mapped[list["TeamMembers"]] = relationship(back_populates="user")


class TeamMembers(Base):
    member_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    role: Mapped[Role] = mapped_column()

    team: Mapped["Team"] = relationship(back_populates="teammembers")