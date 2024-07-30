from pydantic import BaseModel


class CreateTagRequestSchema(BaseModel):
    name: str
    slug: str