


from typing import Any
from domain.entities.tags import Tag
from domain.values.base import Slug, Title


def convert_tag_entity_to_dict(tag: Tag) -> dict[str, Any]:
    return {
        '_id': tag.id,
        'name': tag.name.as_generic_type(),
        'slug': tag.slug.as_generic_type(),
    }


def convert_tag_dict_to_entity(tag: dict[str, Any]) -> Tag:
    return Tag(
        id=tag['_id'],
        name=Title(tag['name']),
        slug=Slug(tag['slug'])
    )