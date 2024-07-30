from uuid import UUID
from pydantic import BaseModel

from application.api.schemas import BaseQueryResponseSchema
from domain.entities.tags import Tag





class TagDetailSchema(BaseModel):
    id: UUID
    name: str
    slug: str

    @classmethod
    def from_entity(cls, tag: Tag) -> 'TagDetailSchema':
        return cls(
            id=tag.id,
            name=tag.name.as_generic_type(),
            slug=tag.slug.as_generic_type(),
        )


class GetAllTagsQueryResponseSchema(BaseQueryResponseSchema[list[TagDetailSchema]]):
    ...