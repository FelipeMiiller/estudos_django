# https://hub.asimov.academy/tutorial/qual-a-diferenca-entre-str-e-repr-em-python/

from abc import ABC
from dataclasses import dataclass, field
from typing import Any, Optional
import uuid
from datetime import datetime
from shared.domain.exceptions import InvalidDateException, InvalidUuidException


@dataclass(frozen=True, slots=True, kw_only=True)
class DefaultEntity(ABC):
    """Default entity"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: Optional[datetime] = field(default_factory=datetime.now)

    def __post_init__(self):
        id_value = str(self.id) if isinstance(self.id, uuid.UUID) else self.id
        # ignore immutable  "frozen=True"
        object.__setattr__(self, "id", id_value)
        created_at_value = datetime.now() if self.created_at is None else self.created_at
        # ignore immutable  "frozen=True"
        object.__setattr__(self, "created_at", created_at_value)
        self.__validate_id__()
        self.__validate_created_at__()

    def __validate_id__(self):
        try:
            uuid.UUID(str(self.id))
        except ValueError as exc:
            raise InvalidUuidException() from exc

    def __validate_created_at__(self):
        if not isinstance(self.created_at, datetime):
            raise InvalidDateException()

    def _set(self, key: str, value: Any):
        object.__setattr__(self, key, value)
        return self
