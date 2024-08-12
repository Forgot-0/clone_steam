from punq import Container, Scope

from fastapi_mail import ConnectionConfig, FastMail
from infra.email.base import EmailBackend
from motor.motor_asyncio import AsyncIOMotorClient
from infra.message_broker.base import BaseMessageBroker
from infra.repositories.developer.base import BaseDeveloperRepository
from infra.repositories.game.base import BaseGameRepository
from infra.repositories.languages.base import BaseLanguageRepository
from infra.repositories.tags.base import BaseTagRepository
from logic.depends.init_mediator import init_mediator
from logic.depends.init_broker import create_message_broker
from logic.depends.init_repositories import (
    init_mongo_developer_repository, 
    init_mongo_game_repository, 
    init_mongo_language_repository, 
    init_mongo_tag_repository
)
from logic.mediator.mediator import Mediator
from settings.config import Config




def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)
    config: Config = container.resolve(Config)

    # Email
    container.register(ConnectionConfig, instance=ConnectionConfig(
        MAIL_USERNAME=Config.email.username,
        MAIL_PASSWORD=Config.email.password,
        MAIL_FROM=Config.email.from_email,
        MAIL_PORT=Config.email.port,
        MAIL_SERVER=Config.email.server,
        MAIL_STARTTLS=Config.email.starttls,
        MAIL_SSL_TLS=Config.email.ssl_tls,
        USE_CREDENTIALS=Config.email.use_credentials,
        VALIDATE_CERTS=Config.email.validate_certs,
    ), scope=Scope.singleton)

    container.register(EmailBackend, 
                        instance=FastMail(
                            config=container.resolve(ConnectionConfig)
                        ), 
                        scope=Scope.singleton)

    # Broker
    container.register(BaseMessageBroker, factory=create_message_broker, scope=Scope.singleton)

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
    container.register(Mediator, factory=lambda: init_mediator(container=container))

    return container
