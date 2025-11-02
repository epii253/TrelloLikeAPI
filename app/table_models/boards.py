from typing import TYPE_CHECKING
from .base import Base

if TYPE_CHECKING:
    from .user import User

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class Board(Base):
    __tablename__ = "boards"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner: Mapped[int] = mapped_column(ForeignKey("users.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    name: Mapped[str] = mapped_column()
    