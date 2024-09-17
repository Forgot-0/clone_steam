from dataclasses import dataclass, field

from domain.entities.base import AggregateRoot
from domain.events.developers.activated import ActvatedDeveloperEvent
from domain.events.developers.created import CreatedDeveloperEvent
from domain.events.developers.deleted import DeletedDeveloperEvent
from domain.exception.base import AlreadyDeletedException
from domain.values.base import Email, Name, Slug




@dataclass(eq=False)
class Developer(AggregateRoot):
    name: Name
    slug: Slug
    email: Email
    is_deleted: bool = field(default=False, kw_only=True)
    is_active: bool = field(default=False, kw_only=True)

    @classmethod
    def create_developer(cls, name: Name, slug: Slug, email: Email) -> 'Developer':
        developer = cls(name=name, slug=slug, email=email)

        developer.register_event(CreatedDeveloperEvent(
            id=developer.id,
            name=developer.name.as_generic_type(),
            slug=developer.slug.as_generic_type(),
            email=developer.email.as_generic_type()
            )
        )

        return developer

    def delete(self) -> None:
        if self.is_deleted:
            raise AlreadyDeletedException()

        self.is_deleted = True
        self.is_active = False
        self.name = Name(None)

        self.register_event(DeletedDeveloperEvent(id=self.id))
    
    def activate(self) -> None:
        if self.is_active:
            raise 
        self.is_active = True

        self.register_event(ActvatedDeveloperEvent(
            id=self.id,
            name=self.name,
            slug=self.slug,
            email=self.email
        ))