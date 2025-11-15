from uuid import UUID

from pydantic import Field

from app.extenshions.database.table_models.team import Role
from app.schemes.responces.base_responce import Informative


class TeamCreationResponceModel(Informative):
    name: str = Field(min_length=5, max_length=30)
    owner_name: str = Field(min_length=3, max_length=16)
    owner_id: UUID = Field()
    team_id: UUID = Field()

class InviteResponceModel(Informative):
    inviter_name: str = Field(min_length=3, max_length=16)
    inviter_id: UUID = Field()
    new_member_id: UUID = Field()
    new_member_name: str = Field(min_length=3, max_length=16)
    team_id: UUID = Field()

class RoleUpdateResponceModel(Informative):
    initiator: str = Field(min_length=3, max_length=16)
    target_id: UUID = Field()
    new_role: Role
    team_id: UUID = Field()

class BoardsInfoResponceModel(Informative):
    boards: list[str]
    team: str = Field(min_length=5, max_length=30)
    team_id: UUID = Field()
