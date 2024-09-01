from dataclasses import dataclass
from typing import Iterable
from uuid import UUID

from domain.entities.games import Game
from infra.repositories.base import BaseMongoDBRepository
from infra.repositories.filters import GetGamesFiltersInfra, PaginationInfra
from infra.repositories.game.base import BaseGameRepository
from infra.repositories.game.mongo.converters import convert_game_dict_to_entity, convert_game_entity_to_dict


@dataclass
class MongoGameRepository(BaseMongoDBRepository, BaseGameRepository):

    async def create(self, game: Game) -> None:
        game_dict = convert_game_entity_to_dict(game=game)
        await self._collection.insert_one(document=game_dict)

    async def get_by_id(self, id: UUID) -> Game | None:
        game = await self._collection.find_one({'_id': id})
        if game:
            return convert_game_dict_to_entity(game)

    async def get_all(self, pagination: PaginationInfra) -> tuple[Iterable[Game], int]:
        games = await self._collection.find({'is_deleted': False}) \
            .skip(pagination.offset).limit(pagination.limit).to_list(length=None)

        count = await self._collection.count_documents({'is_deleted': False})

        return [convert_game_dict_to_entity(game) for game in games], count

    async def check_exists_by_name(self, title: str) -> bool:
        game = await self._collection.find_one({'title': title})
        return bool(game)

    async def get_games(self, filters: GetGamesFiltersInfra, pagination: PaginationInfra) -> tuple[Iterable[Game], int]:
        filter_dict = {
            'is_deleted': False
        }

        if filters.title is not None:
            filter_dict['title'] = filters.title

        if filters.developer_id is not None:
            filter_dict['developer._id'] = filters.developer_id

        if filters.tags:
            filter_dict['tags._id'] = {'$all': filters.tags}

        if filters.languages:
            filter_dict['languages._id'] = {'$all': filters.languages}

        games = await self._collection.find(filter_dict) \
            .skip(pagination.offset).limit(pagination.limit).to_list(length=None)

        count = await self._collection.count_documents(filter=filter_dict)

        return [convert_game_dict_to_entity(game) for game in games], count

    async def delete_by_developer_id(self, id: UUID) -> None:
        await self._collection.update_many({'developer._id': id}, update={"$set": {'is_deleted': True}})

    async def delete_by_id(self, id: UUID) -> None:
        await self._collection.update_one({'_id': id}, update={"$set": {'is_deleted': True}})
