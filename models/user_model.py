from pydantic import Field

from models.base_model import BaseSchema


class UserSchema(BaseSchema):
    id: int
    username: str
    first_name: str | None = Field(None)
    last_name: str | None = Field(None)
    email: str
    password: str
    phone: str | None = Field(None)
    user_status: int = Field(alias="userStatus")
