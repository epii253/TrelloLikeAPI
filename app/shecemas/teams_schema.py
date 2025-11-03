from typing import Optional

from pydantic import BaseModel, Field

class NewTeamModel(BaseModel):
    name: str = Field(min_length=5, max_length=30)

class InviteUserModel(BaseModel):
    username: str = Field(min_length=3, max_length=16)