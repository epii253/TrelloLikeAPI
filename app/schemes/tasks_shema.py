from uuid import UUID

from pydantic import BaseModel, Field

from app.extenshions.database.table_models.tasks import Status


class CreateTaskModel(BaseModel):
    status: Status

    team_id: UUID = Field()
    board_id: UUID = Field()

    tittle: str = Field(min_length=3, max_length=64)
    description: str | None = Field(None, max_length=256)

class UpdateTaskStatusModel(BaseModel):
    team_id: UUID = Field()
    board_id: UUID = Field()

    task_id: UUID = Field()

    new_status: Status

