from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .base import Base
    from .user import User

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

class Board(Base):
    __tablename__ = "Boards"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner: Mapped[int] = mapped_column(ForeignKey("user.id"))
    name: Mapped[str] = mapped_column()
    