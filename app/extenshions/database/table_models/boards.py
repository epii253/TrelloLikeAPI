from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.extenshions.database.table_models.base import Base


class Board(Base):
    __tablename__ = "boards"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    owner: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    team_id: Mapped[UUID] = mapped_column(ForeignKey("teams.id"))
    name: Mapped[str] = mapped_column(unique=True)
    