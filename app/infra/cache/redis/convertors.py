from dataclasses import asdict
from json import dumps
from domain.entities.base import BaseEntity


def convert_entity_to_dict(entity: BaseEntity) -> str:
    data = asdict(entity)
    return dumps(data)

def convert_entities_to_list(entities: list[BaseEntity], count: int) -> str:
    data = [asdict(entity) for entity in entities] + [count]
    return dumps(data)

def convert_dict_to_entity(data: dict, type_cls: BaseEntity) -> BaseEntity:
    return type_cls(**data)

def convert_list_to_entities(data: list, type_cls: BaseEntity) -> list[BaseEntity]:
    return [type_cls(**entity) for entity in data[:-1]] + [int(data[-1])]