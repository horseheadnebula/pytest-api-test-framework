from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",  # игнор лишних полей от API
    )


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
    photo_urls: list[str] | None = Field(default_factory=list)
    tags: list[Tags] | None = Field(default_factory=list)
    status: str
