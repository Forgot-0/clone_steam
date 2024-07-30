from dataclasses import dataclass, field

from domain.entities.base import AggregateRoot
from domain.events.developers.developer_created import NewDeveloperCreated
from domain.events.developers.developer_deleted import DeleteDeveloper
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

        developer.register_event(NewDeveloperCreated(
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
        self.name = Name(None)

        self.register_event(DeleteDeveloper(id=self.id))