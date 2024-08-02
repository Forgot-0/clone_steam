from functools import lru_cache
from motor.motor_asyncio import AsyncIOMotorClient
from punq import Container, Scope

from infra.repositories.developer.mongo.repository import MongoDeveloperRepository
from infra.repositories.game.mongo.repository import MongoGameRepository
from infra.repositories.languages.mongo.repository import MongoLanguageRepository
from infra.repositories.tags.mongo.repository import MongoTagRepository
from settings.config import Config
from infra.repositories.developer.base import BaseDeveloperRepository
from infra.repositories.game.base import BaseGameRepository
from infra.repositories.languages.base import BaseLanguageRepository
from infra.repositories.tags.base import BaseTagRepository
from logic.commands.developers.create import CreateDeveloperCommand, CreateDeveloperCommandHandler
from logic.commands.developers.delete import DeleteDeveloperCommand, DeleteDeveloperCommandHandler
from logic.commands.games.create import CreateGameCommand, CreateGameCommandHandler
from logic.commands.languages.create import CreateLanguageCommand, CreateLanguageCommandHandler
from logic.commands.tags.create import CreateTagCommand, CreateTagCommandHandler
from logic.mediator.event_mediator import EventMediator
from logic.mediator.mediator import Mediator
from logic.queries.developers.detail import DetailDeveloperQuery, DetailDevelopersQueryHandler
from logic.queries.developers.get_all import GetAllDevelopersQueryHandler, GetAllDevelopersQuery
from logic.queries.games.detail import DetailGameQuery, DetailGameQueryHandler
from logic.queries.games.get_all import GetAllGameQuery, GetAllGameQueryHandler
from logic.queries.games.get_games import GetGamesFilterQuery, GetGamesFilterQueryHandler
from logic.queries.languages.get_all import GetAllLanguageQuery, GetAllLanguageQueryHandler
from logic.queries.tags.get_all import GetAllTagsQuery, GetAllTagsQueryHandler




@lru_cache(1)
def init_container() -> Container:
    return _init_container()

def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)

    config: Config = container.resolve(Config)

    def create_mongodb_client():
        return AsyncIOMotorClient(
            config.db.url,
            serverSelectionTimeoutMS=3000,
            uuidRepresentation='standard'
        )

    container.register(AsyncIOMotorClient, factory=create_mongodb_client, scope=Scope.singleton)
    client = container.resolve(AsyncIOMotorClient)

    def init_mongo_developer_repository() -> BaseDeveloperRepository:
        return MongoDeveloperRepository(
            mongo_db_client=client,
            mongo_db_db_name='test',
            mongo_db_collection_name='developers',
        )

    def init_mongo_game_repository() -> BaseGameRepository:
        return MongoGameRepository(
            mongo_db_client=client,
            mongo_db_db_name='test',
            mongo_db_collection_name='games',
        )
    
    def init_mongo_tag_repository() -> BaseTagRepository:
        return MongoTagRepository(
            mongo_db_client=client,
            mongo_db_db_name='test',
            mongo_db_collection_name='tags'
        )

    def init_mongo_language_repository() -> BaseLanguageRepository:
        return MongoLanguageRepository(
            mongo_db_client=client,
            mongo_db_db_name='test',
            mongo_db_collection_name='languages'
        )

    container.register(BaseGameRepository, factory=init_mongo_game_repository, scope=Scope.singleton)
    container.register(BaseDeveloperRepository, factory=init_mongo_developer_repository, scope=Scope.singleton)
    container.register(BaseTagRepository, factory=init_mongo_tag_repository, scope=Scope.singleton)
    container.register(BaseLanguageRepository, factory=init_mongo_language_repository, scope=Scope.singleton)


    #Game
    container.register(CreateGameCommandHandler)

    container.register(GetAllGameQueryHandler)
    container.register(DetailGameQueryHandler)
    container.register(GetGamesFilterQueryHandler)

    #Developer
    container.register(CreateDeveloperCommandHandler)
    container.register(DeleteDeveloperCommandHandler)

    container.register(GetAllDevelopersQueryHandler)
    container.register(DetailDevelopersQueryHandler)

    #Tag
    container.register(CreateTagCommandHandler)
    container.register(GetAllTagsQueryHandler)

    #Language
    container.register(CreateLanguageCommandHandler)
    container.register(GetAllLanguageQueryHandler)


    def init_mediator() -> Mediator:
        mediator = Mediator()

        container.register(EventMediator, instance=mediator)

        #Game
        mediator.register_command(
            CreateGameCommand,
            [container.resolve(CreateGameCommandHandler)]
        )

        mediator.register_query(
            DetailGameQuery,
            container.resolve(DetailGameQueryHandler),
        )

        mediator.register_query(
            GetAllGameQuery,
            container.resolve(GetAllGameQueryHandler),
        )

        mediator.register_query(
            GetGamesFilterQuery,
            container.resolve(GetGamesFilterQueryHandler),
        )


        #Developer
        mediator.register_command(
            CreateDeveloperCommand,
            [container.resolve(CreateDeveloperCommandHandler)],
        )

        mediator.register_command(
            DeleteDeveloperCommand,
            [container.resolve(DeleteDeveloperCommandHandler)],
        )

        mediator.register_query(
            GetAllDevelopersQuery,
            container.resolve(GetAllDevelopersQueryHandler),
        )

        mediator.register_query(
            DetailDeveloperQuery,
            container.resolve(DetailDevelopersQueryHandler),
        )


        #Tag
        mediator.register_command(
            CreateTagCommand,
            [container.resolve(CreateTagCommandHandler)]
        )

        mediator.register_query(
            GetAllTagsQuery,
            container.resolve(GetAllTagsQueryHandler),
        )


        #Language
        mediator.register_command(
            CreateLanguageCommand,
            [container.resolve(CreateLanguageCommandHandler)]
        )

        mediator.register_query(
            GetAllLanguageQuery,
            container.resolve(GetAllLanguageQueryHandler)
        )

        return mediator

    container.register(Mediator, factory=init_mediator)
    return container