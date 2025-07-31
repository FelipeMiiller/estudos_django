from dataclasses import FrozenInstanceError, is_dataclass
from datetime import datetime
import pytest
from category.domain.category_entities import Category
from unittest.mock import patch

from shared.domain.exceptions import ValidationException


def test_create_with_invalid_cases_for_name_prop():
    with pytest.raises(ValidationException) as assert_error:
        Category(name=None)
    assert "The field name is required" in str(assert_error.value)

    with pytest.raises(ValidationException) as assert_error:
        Category(name="")
    assert "The field name is required" in str(assert_error.value)

    with pytest.raises(ValidationException) as assert_error:
        Category(name=123)
    assert "The field name must be a string" in str(assert_error.value)

    with pytest.raises(ValidationException) as assert_error:
        Category(name="r" * 256)
    assert "The field name must be less than 255 characters" in str(
        assert_error.value)


def test_create_with_cases_for_description_prop():
    with pytest.raises(ValidationException) as assert_error:
        Category(name="Movie", description=5)
    assert "The field description must be a string" in str(assert_error.value)


def test_create_with_cases_for_is_active_prop():
    with pytest.raises(ValidationException) as assert_error:
        Category(name="Movie", is_active=None)
    assert "The field is_active must be a boolean" in str(assert_error.value)


def test_create_with_valid_cases():

    try:
        Category(name="Movie")
        Category(name="Movie", description="Some description")
        Category(name="Movie", description="")
        Category(name="Movie", description=None)
        Category(name="Movie", is_active=True)
        Category(name="Movie", is_active=False)
        Category(name="Movie", description="Some description", is_active=True)

    except ValidationException as assert_error:
        pytest.fail(f"Should not raise an exception: {assert_error}")


def test_update_with_invalid_cases_for_name_prop():
    category = Category(name="Movie")
    with pytest.raises(ValidationException) as assert_error:
        category.update(None, "Some description")
    assert "The field name is required" in str(assert_error.value)

    with pytest.raises(ValidationException) as assert_error:
        category.update("", "Some description")
    assert "The field name is required" in str(assert_error.value)

    with pytest.raises(ValidationException) as assert_error:
        category.update(123, "Some description")
    assert "The field name must be a string" in str(assert_error.value)

    with pytest.raises(ValidationException) as assert_error:
        category.update("r" * 256, "Some description")
    assert "The field name must be less than 255 characters" in str(
        assert_error.value)


def test_update_with_cases_for_description_prop():
    category = Category(name="Movie")
    with pytest.raises(ValidationException) as assert_error:
        category.update("Movie", 5)
    assert "The field description must be a string" in str(assert_error.value)


def test_update_with_valid_cases():
    category = Category(name="Movie")

    try:
        category.update("Movie1", "Some description")
        category.update("Movie2", "")
        category.update("Movie3", None)

    except ValidationException as assert_error:
        pytest.fail(f"Should not raise an exception: {assert_error}")
