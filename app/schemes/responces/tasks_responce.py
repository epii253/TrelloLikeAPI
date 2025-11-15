from uuid import UUID

from pydantic import Field

from app.extenshions.database.table_models.tasks import Status
from app.schemes.responces.base_responce import Informative


class CreationTaskResponceModel(Informative):
    task_status: Status

    team: str = Field(min_length=5, max_length=30)

    team_id: UUID = Field()
    task_id: UUID = Field()

    tittle: str = Field(min_length=3, max_length=64)

class UpdateTaskStatusResponceModel(Informative):
    tittle: str = Field(min_length=3, max_length=64)

    new_status: Status