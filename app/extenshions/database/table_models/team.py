from enum import Enum
from functools import total_ordering
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


@total_ordering
class OrderedStrEnum(str, Enum):
    def __lt__(self, other) -> bool:
        if type(self) is type(other):
            members = list(type(self))
            return members.index(self) < members.index(other)
        return NotImplemented

    def __gt__(self, other) -> bool:
        if type(self) is type(other):
            members = list(type(self))
            return members.index(self) > members.index(other)
        return NotImplemented


class Role(OrderedStrEnum):
    Worker = "worker"
    Admin  = "admin"
    Owner  = "owner"


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(unique=True) 

class TeamMember(Base):
    __tablename__ = "team_members"

    member_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    team_id: Mapped[UUID] = mapped_column(ForeignKey("teams.id"), primary_key=True)
    role: Mapped[Role] = mapped_column()