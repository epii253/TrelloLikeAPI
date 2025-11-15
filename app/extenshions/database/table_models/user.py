from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column

from app.extenshions.database.table_models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column()

    hashed_password: Mapped[str] = mapped_column()
    salt: Mapped[str] = mapped_column()

    surename: Mapped[Optional[str]] = mapped_column()
