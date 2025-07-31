from dataclasses import FrozenInstanceError, is_dataclass
from datetime import datetime
import pytest
from category.domain.category_entities import Category
from unittest.mock import patch


def test_if_is_a_dataclass():
    """should return true when Category is a dataclass"""
    assert is_dataclass(Category)


def test_is_immutable_category():
    """should immutable entity"""
    with patch.object(Category, 'validate') as mock_validate_method:
        with pytest.raises(FrozenInstanceError):
            entity = Category(name="Movie")
            entity.name = "not-a-movie"


def test_category_constructor():
    """should return a category when constructor is called"""
    with patch.object(Category, 'validate') :

        category = Category(name="Movie")
        assert category.name == 'Movie'
        assert category.description is None
        assert category.is_active is True
        assert isinstance(category.created_at, datetime)

        created_at = datetime.now()
        category = Category(
            name='Movie',
            description='Some description',
            is_active=True,
            created_at=created_at
        )

    assert category.name == 'Movie'
    assert category.description == 'Some description'
    assert category.is_active is True
    assert isinstance(category.created_at, datetime)


def test_if_created_at_is_generate_in_constructor():
    """should return a category with different timestamps when constructor is called"""
    with patch.object(Category, 'validate') :
        category1 = Category(name='Movie1')
        category2 = Category(name='Movie2')
        assert category1.created_at.timestamp() != category2.created_at.timestamp()


def test_category_update():
    """should update category when update is called"""
    with patch.object(Category, 'validate') :
        category = Category(name="Movie")
        category.update(name="Movie2", description="Some description")
        assert category.name == 'Movie2'
        assert category.description == 'Some description'


def test_category_activate():
    """should activate category when activate is called"""
    with patch.object(Category, 'validate'):
        category = Category(name="Movie")
        category.activate()
        assert category.is_active is True


def test_category_deactivate():
    """should deactivate category when deactivate is called"""
    with patch.object(Category, 'validate') :
        category = Category(name="Movie")
        category.deactivate()
        assert category.is_active is False
