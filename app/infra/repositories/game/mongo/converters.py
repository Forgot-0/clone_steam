from typing import Any
from domain.entities.games import Game
from domain.values.base import Text, Title, Url
from infra.repositories.developer.mongo.converters import (
    convert_developer_entity_to_dict, 
    convert_developer_mapping_to_entity
)
from infra.repositories.languages.mongo.converters import (
    convert_language_dict_to_entity, 
    convert_language_entity_to_dict
)
from infra.repositories.tags.mongo.converters import convert_tag_dict_to_entity, convert_tag_entity_to_dict


def convert_game_entity_to_dict(game: Game) -> dict[str, Any]:
    return {
        '_id': game.id,
        'title': game.title.as_generic_type(),
        'description': game.description.as_generic_type(),
        'release_date': game.release_date,
        'developer': convert_developer_entity_to_dict(developer=game.developer),
        'medias': [media.as_generic_type() for media in game.medias],
        'tags': [convert_tag_entity_to_dict(tag) for tag in game.tags],
        'languages': [convert_language_entity_to_dict(language) for language in game.languages]
    }


def convert_game_dict_to_entity(game_dict: dict[str, Any]):
    game = Game(
        id=game_dict['_id'],
        title=Title(game_dict['title']),
        description=Text(game_dict['description']),
        developer=convert_developer_mapping_to_entity(game_dict['developer']),
        release_date=game_dict['release_date'],
    )

    game.add_medias(Url(media) for media in game_dict.get('medias', []))
    game.add_languages(convert_language_dict_to_entity(language) for language in game_dict.get('languages', []))
    game.add_tags(convert_tag_dict_to_entity(tag) for tag in game_dict.get('tags', []))

    return game