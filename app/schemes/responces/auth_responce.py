from .base_responce import Informative

from pydantic import Field

class AuthResponceModel(Informative):
    token: str = Field(pattern="^(ey).+")