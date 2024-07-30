

from dataclasses import dataclass
from typing import Iterable

from domain.entities.languages import Language
from infra.repositories.filters import PaginationInfra
from infra.repositories.languages.base import BaseLanguageRepository
from logic.queries.base import BaseQuery, BaseQueryHandler


@dataclass(frozen=True)
class GetAllLanguageQuery(BaseQuery):
    pagination: PaginationInfra


@dataclass(frozen=True)
class GetAllLanguageQueryHandler(BaseQueryHandler[GetAllLanguageQuery, tuple[Iterable[Language], int]]):
    language_repository: BaseLanguageRepository

    async def handle(self, query: GetAllLanguageQuery) -> tuple[Iterable[Language], int]:
        languages, count = await self.language_repository.get_all(query.pagination)
        return languages, count