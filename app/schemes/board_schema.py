from uuid import UUID

from pydantic import BaseModel, Field


class CreateBoardModel(BaseModel):
    name: str = Field(min_length=5, max_length=30)
    team_id: UUID = Field()

class GetBoardTasksdModel(BaseModel):
    team_id: UUID = Field()

class DeleteBoardModel(BaseModel):
    board_id: UUID = Field()
    team_id: UUID = Field()