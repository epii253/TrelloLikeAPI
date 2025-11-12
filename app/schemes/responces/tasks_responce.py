from .base_responce import Informative
from ...extenshions.database.table_models.tasks import Status

from pydantic import Field

class CreationTaskResponceModel(Informative):
    task_status: Status

    team: str = Field(min_length=5, max_length=30)
    board: str = Field(min_length=5, max_length=30)

    tittle: str = Field(min_length=3, max_length=64)

class UpdateStatusResponceModel(Informative):
    tittle: str = Field(min_length=3, max_length=64)

    new_status: Status