from pydantic import BaseModel, Field

class RegistrateModel(BaseModel):
    username: str = Field(min_length=5, max_length=22)
    password: str = Field(min_length=5, max_length=40)

    name: str = Field(min_length=5, max_length=16)
    surename: str | None = Field(min_length=5, max_length=16, nullable=True)

class LoginModel(BaseModel):
    username: str = Field(min_length=5, max_length=22)
    password: str = Field(min_length=5, max_length=40)