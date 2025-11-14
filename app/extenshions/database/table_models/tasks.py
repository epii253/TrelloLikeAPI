from enum import Enum
from functools import total_ordering

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


@total_ordering
class OrderedStrEnum(str, Enum):
    def __lt__(self, other):
        if type(self) is type(other):
            members = list(type(self))
            return members.index(self) < members.index(other)
        return NotImplemented

    def __gt__(self, other):
        if type(self) is type(other):
            members = list(type(self))
            return members.index(self) > members.index(other)
        return NotImplemented


class Status(OrderedStrEnum):
    ToDO = "ToDo"
    InProcess = "InProcess" 
    Done = "Done"

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    board_id: Mapped[int] = mapped_column(ForeignKey("boards.id"))

    status: Mapped[Status] = mapped_column()
    tittle: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    
    