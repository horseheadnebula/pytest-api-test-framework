from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",  # игнор лишних полей от API
    )


class UserSchema(BaseSchema):
    id: int
    username: str
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    email: str
    password: str
    phone: str | None = Field(None)
    user_status: int = Field(alias="userStatus")
