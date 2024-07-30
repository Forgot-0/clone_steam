from dataclasses import dataclass
from typing import Iterable, Optional
from uuid import UUID


@dataclass
class PaginationInfra:
    limit: int = 10
    offset: int = 0


@dataclass
class GetGamesFiltersInfra:
    title: Optional[str]
    developer_id: Optional[UUID]
    tags: Optional[Iterable[UUID]]
    languages: Optional[Iterable[UUID]]
