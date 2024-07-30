from dataclasses import dataclass
from typing import Iterable
from domain.entities.tags import Tag
from infra.repositories.filters import PaginationInfra
from infra.repositories.tags.base import BaseTagRepository
from logic.queries.base import BaseQuery, BaseQueryHandler


@dataclass(frozen=True)
class GetAllTagsQuery(BaseQuery):
    pagination: PaginationInfra


@dataclass(frozen=True)
class GetAllTagsQueryHandler(BaseQueryHandler[GetAllTagsQuery, tuple[Iterable[Tag], int]]):
    tag_repository: BaseTagRepository
    
    async def handle(self, query: GetAllTagsQuery) -> tuple[Iterable[Tag], int]:
        tags, count = await self.tag_repository.get_all(query.pagination)
        return tags, count