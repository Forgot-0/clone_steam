from punq import Container
from domain.events.developers.activated import ActvatedDeveloperEvent
from domain.events.developers.created import CreatedDeveloperEvent
from domain.events.developers.deleted import DeletedDeveloperEvent
from logic.commands.developers.activate import ActivateEmailCommand, ActivateEmailCommandHandler
from logic.commands.developers.create import CreateDeveloperCommand, CreateDeveloperCommandHandler
from logic.commands.developers.delete import DeleteDeveloperCommand, DeleteDeveloperCommandHandler
from logic.commands.developers.resend_activation_email import (
    ResendActivationEmailCommand, 
    ResendActivationEmailCommandHandler
)
from logic.commands.games.create import CreateGameCommand, CreateGameCommandHandler
from logic.commands.games.delete import DeleteGameCommand, DeleteGameCommandHandler
from logic.commands.languages.create import CreateLanguageCommand, CreateLanguageCommandHandler
from logic.commands.tags.create import CreateTagCommand, CreateTagCommandHandler
from logic.events.base import PublisherEventHandler
from logic.events.developer.created import NewDeveloperCreatedEventHander
from logic.events.developer.deleted import DeletedDeveloperEventHandler
from logic.queries.developers.detail import DetailDeveloperQuery, DetailDevelopersQueryHandler
from logic.queries.developers.get_all import GetAllDevelopersQueryHandler, GetAllDevelopersQuery
from logic.queries.games.detail import DetailGameQuery, DetailGameQueryHandler
from logic.queries.games.get_all import GetAllGameQuery, GetAllGameQueryHandler
from logic.queries.games.get_games import GetGamesFilterQuery, GetGamesFilterQueryHandler
from logic.queries.languages.get_all import GetAllLanguageQuery, GetAllLanguageQueryHandler
from logic.queries.tags.get_all import GetAllTagsQuery, GetAllTagsQueryHandler
from logic.mediator.mediator import Mediator
from logic.mediator.event_mediator import EventMediator



def init_mediator(container: Container) -> Mediator:
    container.register(PublisherEventHandler)

    #Game
    container.register(CreateGameCommandHandler)
    container.register(DeleteGameCommandHandler)

    container.register(GetAllGameQueryHandler)
    container.register(DetailGameQueryHandler)
    container.register(GetGamesFilterQueryHandler)

    #Developer
    container.register(CreateDeveloperCommandHandler)
    container.register(DeleteDeveloperCommandHandler)
    container.register(ActivateEmailCommandHandler)
    container.register(ResendActivationEmailCommandHandler)

    container.register(GetAllDevelopersQueryHandler)
    container.register(DetailDevelopersQueryHandler)

    container.register(NewDeveloperCreatedEventHander)
    container.register(DeletedDeveloperEventHandler)


    #Tag
    container.register(CreateTagCommandHandler)
    container.register(GetAllTagsQueryHandler)

    #Language
    container.register(CreateLanguageCommandHandler)
    container.register(GetAllLanguageQueryHandler)

    mediator = Mediator()

    container.register(EventMediator, instance=mediator)

    #Game
    mediator.register_command(CreateGameCommand, [container.resolve(CreateGameCommandHandler)])
    mediator.register_command(DeleteGameCommand, [container.resolve(DeleteGameCommandHandler)])


    mediator.register_query(DetailGameQuery, container.resolve(DetailGameQueryHandler))
    mediator.register_query(GetAllGameQuery, container.resolve(GetAllGameQueryHandler))
    mediator.register_query(GetGamesFilterQuery, container.resolve(GetGamesFilterQueryHandler))

    #Developer
    mediator.register_command(CreateDeveloperCommand, [container.resolve(CreateDeveloperCommandHandler)])
    mediator.register_command(DeleteDeveloperCommand, [container.resolve(DeleteDeveloperCommandHandler)])
    mediator.register_command(ActivateEmailCommand, [container.resolve(ActivateEmailCommandHandler)])
    mediator.register_command(ResendActivationEmailCommand, [container.resolve(ResendActivationEmailCommandHandler)])

    mediator.register_query(GetAllDevelopersQuery, container.resolve(GetAllDevelopersQueryHandler))
    mediator.register_query(DetailDeveloperQuery, container.resolve(DetailDevelopersQueryHandler))

    mediator.register_event(
        CreatedDeveloperEvent,
        [
            container.resolve(PublisherEventHandler),
            container.resolve(NewDeveloperCreatedEventHander)
        ]
        )

    mediator.register_event(
        DeletedDeveloperEvent,
        [
            container.resolve(PublisherEventHandler),
            container.resolve(DeletedDeveloperEventHandler)
        ]
        )

    mediator.register_event(
        ActvatedDeveloperEvent,
        [
            container.resolve(PublisherEventHandler),
        ]
        )
    #Tag
    mediator.register_command(CreateTagCommand, [container.resolve(CreateTagCommandHandler)])

    mediator.register_query(GetAllTagsQuery, container.resolve(GetAllTagsQueryHandler))

    #Language
    mediator.register_command(CreateLanguageCommand, [container.resolve(CreateLanguageCommandHandler)])

    mediator.register_query(GetAllLanguageQuery, container.resolve(GetAllLanguageQueryHandler))

    return mediator
