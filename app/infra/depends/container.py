from punq import Container, Scope

from fastapi_mail import ConnectionConfig, FastMail
from redis.asyncio import Redis
from infra.cache.base import BaseCacheService, MemoryCacheService
from infra.email.base import BaseEmailBackend
from motor.motor_asyncio import AsyncIOMotorClient
from infra.email.fasapiemail import FastApiEmailBackend
from infra.message_broker.base import BaseMessageBroker
from infra.repositories.developer.base import BaseDeveloperRepository
from infra.repositories.email.base import BaseEmailRepository
from infra.repositories.game.base import BaseGameRepository
from infra.repositories.languages.base import BaseLanguageRepository
from infra.repositories.tags.base import BaseTagRepository
from infra.depends.init_mediator import init_mediator
from infra.depends.init_broker import create_message_broker
from infra.depends.init_repositories import (
    init_mongo_developer_repository, 
    init_mongo_game_repository, 
    init_mongo_language_repository, 
    init_mongo_tag_repository,
    init_redis_email_repository
)
from logic.mediator.mediator import Mediator
from settings.config import Config




def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)
    config: Config = container.resolve(Config)

    container.register(
        Redis, 
        instance=Redis(
            host=config.redis.host, 
            port=config.redis.port
            )
        )


    #Email Repository
    redis = container.resolve(Redis)

    container.register(BaseEmailRepository, factory=lambda: init_redis_email_repository(redis=redis))

    #Email
    container.register(ConnectionConfig, 
        instance=ConnectionConfig(
            MAIL_USERNAME=config.email.username,
            MAIL_PASSWORD=config.email.password,
            MAIL_FROM=config.email.from_email,
            MAIL_PORT=config.email.port,
            MAIL_SERVER=config.email.server,
            MAIL_STARTTLS=config.email.starttls,
            MAIL_SSL_TLS=config.email.ssl_tls,
            USE_CREDENTIALS=config.email.use_credentials,
            VALIDATE_CERTS=config.email.validate_certs,
        ), 
        scope=Scope.singleton
    )

    def init_fastapimail_email_backend():
        return FastApiEmailBackend(
            fast_mail=FastMail(
                        config=container.resolve(ConnectionConfig)
                    )
            )

    container.register(BaseEmailBackend, 
                        factory=init_fastapimail_email_backend,
                        scope=Scope.singleton)

    # Broker
    container.register(
        BaseMessageBroker,
        factory=lambda: create_message_broker(config=config),
        scope=Scope.singleton
    )

    #Cache
    container.register(BaseCacheService, MemoryCacheService, scope=Scope.singleton)

    # MongoDB
    def create_mongodb_client():
        return AsyncIOMotorClient(
            config.db.url,
            serverSelectionTimeoutMS=3000,
            uuidRepresentation='standard'
        )

    container.register(AsyncIOMotorClient, factory=create_mongodb_client, scope=Scope.singleton)
    client = container.resolve(AsyncIOMotorClient)

    # Repositories
    container.register(
        BaseGameRepository, 
        factory=lambda: init_mongo_game_repository(client),
        scope=Scope.singleton
    )
    container.register(
        BaseDeveloperRepository,
        factory=lambda: init_mongo_developer_repository(client),
        scope=Scope.singleton
    )
    container.register(
        BaseTagRepository, 
        factory=lambda: init_mongo_tag_repository(client),
        scope=Scope.singleton
    )
    container.register(
        BaseLanguageRepository, 
        factory=lambda: init_mongo_language_repository(client),
        scope=Scope.singleton
    )

    # Mediator
    container.register(
        Mediator,
        factory=lambda: init_mediator(container=container)
    )

    return container
