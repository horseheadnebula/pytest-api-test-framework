from typing import Literal

from pydantic import Field

from models.base_model import BaseSchema


class Category(BaseSchema):
    id: int | None = Field(None)
    name: str | None = Field(None)


class Tags(BaseSchema):
    id: int | None = Field(None)
    name: str | None = Field(None)


class PetSchema(BaseSchema):
    id: int
    category: Category | None = Field(None)
    name: str
    photo_urls: list[str] | None = Field(default_factory=list, alias="photoUrls")
    tags: list[Tags] | None = Field(default_factory=list)
    status: Literal["available", "pending", "sold"] = Field(...)
