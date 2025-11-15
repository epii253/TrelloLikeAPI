from uuid import UUID

from pydantic import BaseModel, Field

from app.extenshions.database.table_models.team import Role


class NewTeamModel(BaseModel):
    name: str = Field(min_length=5, max_length=30)

class InviteUserModel(BaseModel):
    user_id: UUID = Field()

class NewRoleModel(BaseModel):
    user_id: UUID = Field()
    role: Role