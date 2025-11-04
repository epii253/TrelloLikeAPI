from ..table_models.tasks import Status

from pydantic import BaseModel, Field

class CreateTaskModel(BaseModel):
    status: Status

    team: str = Field(min_length=5, max_length=30)
    board: str = Field(min_length=5, max_length=30)

    tittle: str = Field(min_length=3, max_length=64)
    description: str | None = Field(None, min_length=3, max_length=256)
