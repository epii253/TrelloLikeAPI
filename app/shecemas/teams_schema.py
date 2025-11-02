from typing import Optional

from pydantic import BaseModel, Field

class NewTeamModel(BaseModel):
    name: str = Field(min_length=5, max_length=30)