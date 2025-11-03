from app.table_models.base import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.table_models.team import TeamMember

from sqlalchemy import ForeignKey, Integer
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)

    hashed_password: Mapped[str] = mapped_column()
    salt: Mapped[str] = mapped_column()

    surename: Mapped[Optional[str]] = mapped_column()

    team_memberships: Mapped[list["TeamMember"]] = relationship(back_populates="user")