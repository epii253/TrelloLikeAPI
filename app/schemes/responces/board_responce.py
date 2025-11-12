from .base_responce import Informative
from ...extenshions.database.table_models.tasks import Status

from pydantic import Field

class BoardCreationResponceModel(Informative):
    board_name: str = Field(min_length=5, max_length=30)
    team_name: str = Field(min_length=5, max_length=30)
    owner_name: str = Field(min_length=3, max_length=16)

class TaskInfoModel(Informative):
    tittle: str = Field(min_length=3, max_length=64)
    status: Status
    description: str | None = Field(None, max_length=256) 

class TasksInfoResponceModel(Informative):
    board_name: str = Field(min_length=5, max_length=30)
    team_name: str = Field(min_length=5, max_length=30)
    tasks: list[TaskInfoModel]