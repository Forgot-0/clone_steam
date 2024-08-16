from uuid import UUID
from pydantic import BaseModel

from application.api.schemas import BaseQueryResponseSchema
from domain.entities.developers import Developer






class DeveloperDetailSchema(BaseModel):
    id: UUID
    name: str
    slug: str
    email: str

    @classmethod
    def from_entity(cls, developer: Developer) -> 'DeveloperDetailSchema':
        return cls(
            id=developer.id,
            name=developer.name.as_generic_type(),
            slug=developer.slug.as_generic_type(),
            email=developer.email.as_generic_type(),
        )


class GetAllDevelopersQueryResponseSchema(BaseQueryResponseSchema[list[DeveloperDetailSchema]]):
    ...