

from dataclasses import dataclass
from typing import Any
from .exceptions import ValidationException


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
        if self.value is not None and not isinstance(self.value, (int, float)) and not isinstance(self.value, bool):
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
