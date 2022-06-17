import pytest

from ..cards import Card
from ..cards import Pos
from ..cards import load_card
from ..cards import save_card


@pytest.mark.parametrize('_class', [*Card.__subclasses__()])
def test_card_class(user, _class):
    card = _class(user, Pos(1, 2))
    assert {
        'type': _class.__name__.lower(),
        'owner': user,
        'x': 1,
        'y': 2,
    } == card.serialize()


@pytest.mark.parametrize('_class', [*Card.__subclasses__()])
def test_load_card(user, _class):
    card = load_card({
        'type': _class.__name__.lower(),
        'owner': user,
        'x': 10,
        'y': 12,
    })
    assert isinstance(card, _class)
    assert card.owner == user
    assert card.pos == Pos(10, 12)
    card = load_card({
        'type': None,
        'owner': user,
        'x': 10,
        'y': 12,
    })
    assert card is None


@pytest.mark.parametrize('_class', [*Card.__subclasses__()])
def test_save_card(user, _class):
    card = _class(user, Pos(1, 2))
    assert card.serialize() == save_card(card)
