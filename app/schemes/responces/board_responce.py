from uuid import UUID

from pydantic import Field

from app.extenshions.database.table_models.tasks import Status
from app.schemes.responces.base_responce import Informative


class BoardCreationResponceModel(Informative):
    board_name: str = Field(min_length=5, max_length=30)
    board_id: UUID = Field()
    team_id: UUID = Field()
    owner_id: UUID = Field()

class TaskInfoModel(Informative):
    tittle: str = Field(min_length=3, max_length=64)
    status: Status
    description: str | None = Field(None, max_length=256) 

class TasksInfoResponceModel(Informative):
    board_name: str = Field(min_length=5, max_length=30)
    board_id: UUID = Field()

    team_name: str = Field(min_length=5, max_length=30)
    team_id: UUID = Field()

    tasks: list[TaskInfoModel]