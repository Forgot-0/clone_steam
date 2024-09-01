from fastapi import APIRouter, Depends, status
from punq import Container
from application.api.schemas import ErrorSchema, Pagination
from application.api.tags.schemas.requests import CreateTagRequestSchema
from application.api.tags.schemas.responses import GetAllTagsQueryResponseSchema, TagDetailSchema
from logic.commands.tags.create import CreateTagCommand
from logic.depends.init import init_container
from logic.mediator.mediator import Mediator
from logic.queries.tags.get_all import GetAllTagsQuery


router = APIRouter(
    prefix='/tag',
    tags=['Tag']
)



@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description='Create Tag',
    responses={
        status.HTTP_201_CREATED: {'model': TagDetailSchema},
    }
)
async def create_tag(
    schema: CreateTagRequestSchema,
    container: Container=Depends(init_container)
) -> TagDetailSchema:
    mediator: Mediator = container.resolve(Mediator)

    tag, *_ = await mediator.handle_command(
        CreateTagCommand(**schema.model_dump())
        )

    return TagDetailSchema.from_entity(tag)

@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    description='Get all tags',
    responses={
        status.HTTP_200_OK: {'model': GetAllTagsQueryResponseSchema},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema}
    }
)
async def get_all_tags(
    filters: Pagination=Depends(),
    container: Container=Depends(init_container)
) -> GetAllTagsQueryResponseSchema:
    mediator: Mediator = container.resolve(Mediator)

    tags, count = await mediator.handle_query(
        GetAllTagsQuery(pagination=filters.to_infra())
        )

    return GetAllTagsQueryResponseSchema(
        items=[TagDetailSchema.from_entity(tag) for tag in tags],
        count=count,
        offset=filters.offset,
        limit=filters.limit
    )