from dataclasses import dataclass
from typing import Iterable
from uuid import UUID

from domain.entities.developers import Developer
from infra.repositories.base import BaseMongoDBRepository
from infra.repositories.developer.base import BaseDeveloperRepository
from infra.repositories.developer.mongo.converters import (
    convert_developer_entity_to_dict, 
    convert_developer_mapping_to_entity
)
from infra.repositories.filters import PaginationInfra



@dataclass
class MongoDeveloperRepository(BaseMongoDBRepository, BaseDeveloperRepository):

    async def check_exists_by_name(self, name: str) -> bool:
        return bool(await self._collection.find_one({'name': name}))

    async def check_exists_by_email(self, email: str) -> bool:
        return bool(await self._collection.find_one({'email': email}))

    async def create(self, developer: Developer) -> None:
        developer_dict = convert_developer_entity_to_dict(developer=developer)
        await self._collection.insert_one(developer_dict)

    async def get_by_id(self, id: UUID) -> Developer | None:
        developer = await self._collection.find_one({'_id': id})

        if developer:
            return convert_developer_mapping_to_entity(developer)

    async def get_by_email(self, email: str) -> Developer | None:
        developer = await self._collection.find_one({'email': email})
        if developer:
            return convert_developer_mapping_to_entity(developer)

    async def delete_by_id(self, id: UUID) -> None:
        await self._collection.update_one({'_id': id}, update={"$set": {'is_deleted': True}})

    async def update(self, developer: Developer) -> None:
        await self._collection.update_one(
            {'_id': developer.id}, 
            update={'$set': convert_developer_entity_to_dict(developer=developer)}
        )

    async def get_all(self, pagination: PaginationInfra) -> tuple[Iterable[Developer], int]:
        developers = await self._collection.find({'is_deleted': False}) \
            .skip(pagination.offset).limit(pagination.limit).to_list(length=None)
        count = await self._collection.count_documents({'is_deleted': False})
        return [convert_developer_mapping_to_entity(developer) for developer in developers], count

    async def activate(self, email: str) -> None:
        await self._collection.update_one({'email': email}, update={"$set": {'is_active': True}})

