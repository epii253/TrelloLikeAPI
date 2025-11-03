from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user import User

from .base import Base
from enum import Enum

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

class Role(Enum):
    Worker = 0
    Admin = 1
    Owner = 2


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(unique=True) 

    members: Mapped[list["TeamMember"]] = relationship(back_populates="team")

    # admins only
    admins: Mapped[list["User"]] = relationship(
        secondary="team_members",
        primaryjoin="Team.id == TeamMember.team_id",
        secondaryjoin=f"and_( \
            TeamMember.member_id == User.id, \
            TeamMember.role == {Role.Admin.value}  \
        )",
        viewonly=True,
        overlaps="members"
    )

    # workers only
    workers: Mapped[list["User"]] = relationship(
        secondary="team_members",
        primaryjoin="Team.id == TeamMember.team_id",
        secondaryjoin=f"and_( \
            TeamMember.member_id == User.id, \
            TeamMember.role == {Role.Worker.value} \
        )",
        viewonly=True,
        overlaps="members"
    )

class TeamMember(Base):
    __tablename__ = "team_members"

    member_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), primary_key=True)
    role: Mapped[Role] = mapped_column()

    user: Mapped["User"] = relationship(back_populates="team_memberships")
    team: Mapped["Team"] = relationship(back_populates="members")