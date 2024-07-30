from datetime import datetime
from typing import Iterable, List, Optional
from uuid import UUID
from pydantic import BaseModel, Field

from infra.repositories.filters import GetGamesFiltersInfra




class CreateGameRequestSchema(BaseModel):
    title: str
    description: str

    release_date: datetime = datetime.now()

    developer_id: UUID
    medias: list[str] = Field(default_factory=list)
    tags: list[UUID] = Field(default_factory=list)
    languages: list[UUID] = Field(default_factory=list)



class GameFilters(BaseModel):
    title: Optional[str] = None
    developer_id: Optional[UUID] = None
    tags: Iterable[UUID] = []
    languages: Iterable[UUID] = []

    def to_infra(self):
        return GetGamesFiltersInfra(
            title=self.title,
            developer_id=self.developer_id,
            tags=self.tags,
            languages=self.languages
        )