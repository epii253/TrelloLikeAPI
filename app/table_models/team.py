from .base import Base
from enum import StrEnum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Role(StrEnum):
    Worker = 'worker'
    Admin = 'admin'
    Owner = 'owner'


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(unique=True) 

class TeamMember(Base):
    __tablename__ = "team_members"

    member_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), primary_key=True)
    role: Mapped[Role] = mapped_column()