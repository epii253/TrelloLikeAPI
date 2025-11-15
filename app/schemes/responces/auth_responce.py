from uuid import UUID

from pydantic import Field

from app.schemes.responces.base_responce import Informative


class AuthResponceModel(Informative):
    token: str = Field(pattern="^(ey).+")
    id: UUID = Field()