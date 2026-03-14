from pydantic import BaseModel, Field


class Category(BaseModel):
    id: int | None = Field(None)
    name: str | None = Field(None)


class Tags(BaseModel):
    id: int | None = Field(None)
    name: str | None = Field(None)


class PetSchema(BaseModel):
    id: int
    category: Category | None = Field(None)
    name: str
    photo_urls: list[str] | None = Field(default_factory=list)
    tags: list[Tags] | None = Field(default_factory=list)
    status: str
