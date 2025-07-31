from dataclasses import dataclass
from typing import Optional
from shared.domain.default_entity import DefaultEntity
from shared.domain.validators import ValidatorRules


@dataclass(frozen=True, slots=True, kw_only=True)
class Category(DefaultEntity):
    name: str
    description: Optional[str] = None
    is_active: bool = True

    def __post_init__(self):
        self.validate(name=self.name, description=self.description, is_active=self.is_active)

    def update(self, name: str, description: str):
        self.validate(name=name, description=description, is_active=self.is_active)
        self._set("name", name)
        self._set("description", description)

    def activate(self):
        self._set("is_active", True)

    def deactivate(self):
        self._set("is_active", False)

    @classmethod
    def validate(cls, name: str, description: str, is_active: bool=None):
        ValidatorRules.validate(
            name, "name").required().string().max_length(255)
        ValidatorRules.validate(description, "description").string()
        ValidatorRules.validate(is_active, "is_active").boolean()
