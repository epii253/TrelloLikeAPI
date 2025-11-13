from .base_responce import Informative
from app.extenshions.database.table_models.team import Role

from pydantic import Field

class TeamCreationResponceModel(Informative):
    name: str = Field(min_length=5, max_length=30)
    owner_name: str = Field(min_length=3, max_length=16)

class InviteResponceModel(Informative):
    inviter_name: str = Field(min_length=3, max_length=16)
    new_member_name: str = Field(min_length=3, max_length=16)
    team: str = Field(min_length=5, max_length=30)

class RoleUpdateResponceModel(Informative):
    initiator: str = Field(min_length=3, max_length=16)
    target_name: str = Field(min_length=3, max_length=16)
    new_role: Role
    team: str = Field(min_length=5, max_length=30)

class BoardsInfoResponceModel(Informative):
    boards: list[str]
    team: str = Field(min_length=5, max_length=30)
