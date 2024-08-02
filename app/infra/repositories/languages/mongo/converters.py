from typing import Any

from domain.entities.languages import Language
from domain.values.base import Slug, Title



def convert_language_entity_to_dict(language: Language) -> dict[str, Any]:
    return {
        '_id': language.id,
        'lang': language.lang.as_generic_type(),
        'slug': language.slug.as_generic_type(),
        'interface': language.interface,
        'full_audio': language.full_audio,
        'subtitles': language.subtitles,
    }


def convert_language_dict_to_entity(language: dict[str, Any]):
    return Language(
        id=language['_id'],
        lang=Title(language['lang']),
        slug=Slug(language['slug']),
        interface=language['interface'],
        full_audio=language['full_audio'],
        subtitles=language['subtitles']
    )