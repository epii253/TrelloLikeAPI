from .base import Base
from .user import User

from enum import Enum
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

class Status(Enum):
    ToDO = 0
    InProcess = 1
    Done = 2

class Task(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    board_id: Mapped[int] = mapped_column(ForeignKey("board.id"))
    
    status: Mapped[Status] = mapped_column()
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    
    