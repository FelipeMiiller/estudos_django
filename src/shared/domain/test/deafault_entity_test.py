from dataclasses import FrozenInstanceError, is_dataclass
import pytest
import uuid
from datetime import datetime
from shared.domain.default_entity import DefaultEntity
from shared.domain.exceptions import InvalidUuidException, InvalidDateException


def test_if_is_a_dataclass():
    """should return true when EntityDefault is a dataclass"""
    assert is_dataclass(DefaultEntity)


def test_entitydefault_creation():
    """should return a entitydefault when constructor is called"""
    entity = DefaultEntity()
    assert isinstance(entity.id, str) or isinstance(entity.id, uuid.UUID)
    assert isinstance(entity.created_at, datetime)


def test_entitydefault_invalid_id():
    """should raise InvalidUuidException when id is not a uuid"""

    with pytest.raises(InvalidUuidException):
        DefaultEntity(id="not-a-uuid")


def test_entity_validate_insert_id():
    """should return a string when id is a uuid"""
    entity = DefaultEntity(id="3b995105-4504-4718-b229-93c6b6a2f388")
    assert entity.id == "3b995105-4504-4718-b229-93c6b6a2f388"
    assert isinstance(entity.id, str)


def test_entity_validate_generate_id():
    """should return a uuid when id is a string uuid"""
    entity = DefaultEntity()
    assert isinstance(entity.id, str)
    assert uuid.UUID(entity.id, version=4)


def test_entitydefault_invalid_created_at():
    """should raise InvalidDateException when created_at is not a datetime"""

    with pytest.raises(InvalidDateException):
        DefaultEntity(created_at="not-a-date")


def test_is_immutable():
    """should immutable entity"""
    with pytest.raises(FrozenInstanceError):
        entity = DefaultEntity()
        entity.id = "not-a-uuid"
        entity.created_at = "not-a-date"


def test_entitydefault_repr():
    """should return a string when repr is called"""
    entity = DefaultEntity()
    assert repr(entity) == f"DefaultEntity(id={entity.id!r}, created_at={entity.created_at!r})"
    