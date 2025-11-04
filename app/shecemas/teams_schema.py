from typing import Optional

from ..table_models.team import Role

from pydantic import BaseModel, Field

class NewTeamModel(BaseModel):
    name: str = Field(min_length=5, max_length=30)

class InviteUserModel(BaseModel):
    username: str = Field(min_length=3, max_length=16)

class NewRoleModel(BaseModel):
    username: str = Field(min_length=3, max_length=16)
    role: Role