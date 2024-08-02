from typing import Any, Mapping

from domain.entities.developers import Developer
from domain.values.base import Email, Name, Slug


def convert_developer_entity_to_dict(developer: Developer) -> dict:
    return {
        '_id': developer.id,
        'name': developer.name.as_generic_type(),
        'slug': developer.slug.as_generic_type(),
        'email': developer.email.as_generic_type(),
        'is_deleted': developer.is_deleted,
        'is_active': developer.is_active
    }


def convert_developer_mapping_to_entity(mapping_developer: dict) -> Developer:
    return Developer(
        id=mapping_developer['_id'],
        name=Name(mapping_developer['name']),
        slug=Slug(mapping_developer['slug']),
        email=Email(mapping_developer['email']),
        is_deleted=mapping_developer['is_deleted'],
        is_active=mapping_developer['is_active']
    )
