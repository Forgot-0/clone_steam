from fastapi import APIRouter, Depends, status
from punq import Container

from application.api.languages.schemas.requests import CreateLanguageRequestSchema
from application.api.languages.schemas.responses import GetAllLanguagesQueryResponseSchema, LanguageDetailSchema
from application.api.schemas import ErrorSchema, Pagination
from logic.commands.languages.create import CreateLanguageCommand
from logic.depends.init import init_container
from logic.mediator.mediator import Mediator
from logic.queries.languages.get_all import GetAllLanguageQuery


router = APIRouter(
    prefix='/language',
    tags=['Language']
)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    description="Create Language",
    responses={
        status.HTTP_201_CREATED: {'model': LanguageDetailSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def create_language(
    schema: CreateLanguageRequestSchema,
    container: Container=Depends(init_container)
) -> LanguageDetailSchema:
    mediator: Mediator = container.resolve(Mediator)

    language, *_ = await mediator.handle_command(
        CreateLanguageCommand(**schema.model_dump()
        )
    )

    return LanguageDetailSchema.from_entity(language=language)

@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    description="Get all languages",
    responses={
        status.HTTP_200_OK: {'model': GetAllLanguagesQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def get_all_languages(
    filters: Pagination=Depends(),
    container: Container=Depends(init_container)
) -> GetAllLanguagesQueryResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    languages, count = await mediator.handle_query(
        GetAllLanguageQuery(pagination=filters.to_infra())
    )

    return GetAllLanguagesQueryResponseSchema(
        items=[LanguageDetailSchema.from_entity(lang) for lang in languages],
        count=count,
        offset=filters.offset,
        limit=filters.limit
    )