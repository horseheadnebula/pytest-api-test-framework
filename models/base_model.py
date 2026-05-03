from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",  # игнор лишних полей от API
    )
