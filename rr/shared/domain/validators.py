

from abc import ABC, abstractmethod

from dataclasses import dataclass
from typing import Any, Dict, Generic, List, TypeVar
from .exceptions import ValidationException
from rest_framework.serializers import Serializer


@dataclass(frozen=True, slots=True)
class ValidatorRules:

    value: Any
    key: str

    @staticmethod
    def validate(value: Any, key: str) -> "ValidatorRules":
        return ValidatorRules(value, key)

    def required(self) -> "ValidatorRules":
        if self.value is None or self.value == "":
            raise ValidationException(f"The field {self.key} is required")
        return self

    def string(self) -> "ValidatorRules":
        if self.value is not None and not isinstance(self.value, str):
            raise ValidationException(f"The field {self.key} must be a string")
        return self

    def number(self) -> "ValidatorRules":
        if self.value is not None and (not isinstance(self.value, (int, float)) or isinstance(self.value, bool)):
            raise ValidationException(
                f"The field {self.key} must be a number")
        return self

    def boolean(self) -> "ValidatorRules":
        if not isinstance(self.value, bool):
            raise ValidationException(
                f"The field {self.key} must be a boolean")
        return self

    def max_length(self, max_length: int) -> "ValidatorRules":
        if len(self.value) > max_length:
            raise ValidationException(
                f"The field {self.key} must be less than {max_length} characters")
        return self

    def min_length(self, min_length: int) -> "ValidatorRules":
        if len(self.value) < min_length:
            raise ValidationException(
                f"The field {self.key} must be at least {min_length} characters")
        return self


ErrorFields = Dict[str, List[str]]
PropsValidated = TypeVar("PropsValidated")  # tipo genérico


@dataclass(slots=True)
class ValidatorFieldsInterface(ABC, Generic[PropsValidated]):

    errors: ErrorFields = None
    validated_data: PropsValidated = None

    @abstractmethod
    def validate(self, data: Any) -> bool:
        raise NotImplementedError()


class DRFValidator(ValidatorFieldsInterface[PropsValidated], ABC):

    def validate(self, data: Serializer):
        if data.is_valid():
            self.validated_data = data.validated_data
            return True
        else:

            self.errors = {
                field: [str(_error) for _error in errors]
                for field, errors in data.errors.items()
            }
            return False
