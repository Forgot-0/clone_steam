from typing import Iterable
from uuid import UUID
from domain.entities.tags import Tag
from infra.repositories.base import BaseMongoDBRepository
from infra.repositories.filters import PaginationInfra
from infra.repositories.tags.base import BaseTagRepository
from infra.repositories.tags.mongo.converters import convert_tag_dict_to_entity, convert_tag_entity_to_dict


class MongoTagRepository(BaseMongoDBRepository, BaseTagRepository):
    async def get_by_id(self, id: UUID) -> Tag | None:
        tag = await self._collection.find_one({'_id': id})
        if tag:
            return convert_tag_dict_to_entity(tag)

    async def create(self, tag: Tag) -> None:
        tag_dict = convert_tag_entity_to_dict(tag)
        await self._collection.insert_one(tag_dict)

    async def get_all(self, pagination: PaginationInfra) -> tuple[Iterable[Tag], int]:
        tags = await self._collection.find().skip(pagination.offset).limit(pagination.limit).to_list(length=None)
        count = await self._collection.count_documents({})
        return [convert_tag_dict_to_entity(tag) for tag in tags], count