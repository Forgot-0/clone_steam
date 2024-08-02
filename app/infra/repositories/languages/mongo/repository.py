from dataclasses import dataclass
from typing import Iterable
from uuid import UUID

from domain.entities.languages import Language
from infra.repositories.base import BaseMongoDBRepository
from infra.repositories.filters import PaginationInfra
from infra.repositories.languages.base import BaseLanguageRepository
from infra.repositories.languages.mongo.converters import (
    convert_language_dict_to_entity, 
    convert_language_entity_to_dict
)


@dataclass
class MongoLanguageRepository(BaseMongoDBRepository, BaseLanguageRepository):

    async def get_by_id(self, id: UUID) -> Language | None:
        result = await self._collection.find_one({'_id': id})
        if result:
            return convert_language_dict_to_entity(language=result)

    async def create(self, language: Language) -> None:
        language_dict = convert_language_entity_to_dict(language=language)
        await self._collection.insert_one(document=language_dict)

    async def get_all(self, pagination: PaginationInfra) -> tuple[Iterable[Language], int]:
        languages = await self._collection.find().skip(pagination.offset).limit(pagination.limit).to_list(length=None)
        count = await self._collection.count_documents({})
        return [convert_language_dict_to_entity(language) for language in languages], count