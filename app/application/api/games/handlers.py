from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from punq import Container

from application.api.games.schemas.requests import CreateGameRequestSchema, GameFilters
from application.api.games.schemas.responses import (
    GameDetailForAllSchema, 
    GameDetailSchema, 
    GetAllGamesQueryResponseSchema
)
from application.api.schemas import ErrorSchema, Pagination
from domain.exception.base import ApplicationException
from logic.commands.games.create import CreateGameCommand
from logic.init import init_container
from logic.mediator.mediator import Mediator
from logic.queries.games.detail import DetailGameQuery
from logic.queries.games.get_all import GetAllGameQuery
from logic.queries.games.get_games import GetGamesFilterQuery


router = APIRouter(
    prefix='/game',
    tags=['Game'],
)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    description='Create game',
    responses={
        status.HTTP_201_CREATED: {'model': GameDetailSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def create_game(
    schema: CreateGameRequestSchema,
    container: Container=Depends(init_container)
) -> GameDetailSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        game, *_ = await mediator.handle_command(
            CreateGameCommand(**schema.model_dump())
        )
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exception.message)

    return GameDetailSchema.from_entity(game=game)

@router.get(
    '/{game_id}',
    status_code=status.HTTP_200_OK,
    description='Get game by id',
    responses={
        status.HTTP_200_OK: {'model': GameDetailSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def get_game_by_id(
    game_id: UUID,
    container: Container=Depends(init_container)
) -> GameDetailSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        developer = await mediator.handle_query(
            DetailGameQuery(game_id=game_id)
        )
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exception.message)

    return GameDetailSchema.from_entity(developer)

@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    description='Get all game',
    responses={
        status.HTTP_200_OK: {'model': GetAllGamesQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def get_all_games(
    pagination: Pagination=Depends(),
    container: Container=Depends(init_container)
) -> GetAllGamesQueryResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        games, count = await mediator.handle_query(
            GetAllGameQuery(pagination=pagination.to_infra())
            )
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exception.message)

    return GetAllGamesQueryResponseSchema(
        items=[GameDetailForAllSchema.from_entity(game) for game in games],
        count=count,
        offset=pagination.offset,
        limit=pagination.limit,
    )


@router.get(
    '/search/',
    status_code=status.HTTP_200_OK,
    description='Get games',
    responses={
        status.HTTP_200_OK: {'model': GetAllGamesQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def get_games(
    filters: GameFilters=Depends(),
    pagination: Pagination=Depends(),
    tags: list[UUID]=Query(default_factory=list),
    languages: list[UUID]=Query(default_factory=list),
    container: Container=Depends(init_container)
) -> GetAllGamesQueryResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    try:
        games, count = await mediator.handle_query(
            GetGamesFilterQuery(
                filters=filters.to_infra(tags=tags, languages=languages), 
                pagination=pagination.to_infra()
                )
            )
    except ApplicationException as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=exception.message)

    return GetAllGamesQueryResponseSchema(
        items=[GameDetailForAllSchema.from_entity(game) for game in games],
        count=count,
        offset=pagination.offset,
        limit=pagination.limit,
    )