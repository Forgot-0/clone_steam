from pydantic import BaseModel


class CreateDeveloperRequestSchema(BaseModel):
    name: str
    slug: str
    email: str


class ActivateDeveloperRequestSchema(BaseModel):
    email: str
    code: str