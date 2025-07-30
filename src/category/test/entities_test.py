from dataclasses import FrozenInstanceError, is_dataclass
from datetime import datetime
from category.domain.entities import Category


def test_if_is_a_dataclass():
    """should return true when Category is a dataclass"""
    assert is_dataclass(Category)




def test_is_immutable():
    """should immutable entity"""
    with pytest.raises(FrozenInstanceError):
        entity = DefaultEntity()
        entity.id = "not-a-uuid"
        entity.created_at = "not-a-date"




def test_category_constructor():
    """should return a category when constructor is called"""
    category = Category(
        name='Movie',

    )
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
    category1 = Category(
        name='Movie1',

    )
    category2 = Category(
        name='Movie2',

    )
    assert category1.created_at.timestamp() != category2.created_at.timestamp()


def test_is_immutable():
    """should immutable entity"""
    with pytest.raises(FrozenInstanceError):
        entity = Category()
        entity.id = "not-a-uuid"
        entity.created_at = "not-a-date"



def test_is_immutable_name():
    """should immutable entity"""
    with pytest.raises(FrozenInstanceError):
        entity = Category(name='test')
        entity.name = "not-a-uuid"
