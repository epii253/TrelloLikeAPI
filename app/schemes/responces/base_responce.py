from typing import Optional

from pydantic import BaseModel, Field


class Informative(BaseModel):
    detail: Optional[str] = Field(None, max_length=8192)