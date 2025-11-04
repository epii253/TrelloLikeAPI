from pydantic import BaseModel, Field

class CreateBoardModel(BaseModel):
    name: str = Field(min_length=5, max_length=30)
    team_name: str = Field(min_length=5, max_length=30)

class DeleteBoardModel(BaseModel):
    name: str = Field(min_length=5, max_length=30)
    team_name: str = Field(min_length=5, max_length=30)