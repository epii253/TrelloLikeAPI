from typing import Optional

from pydantic import BaseModel, Field

class RegistrateModel(BaseModel):
    username: str = Field(min_length=3, max_length=16)
    password: str = Field(min_length=8, max_length=40)

    surename: Optional[str] = Field(None, min_length=5, max_length=16)

class LoginModel(BaseModel):
    username: str = Field(min_length=3, max_length=16)
    password: str = Field(min_length=3, max_length=40)