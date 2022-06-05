import pytest

from core.cards import Card
from core.cards import Pos
from core.cards import load_card
from core.cards import save_card


@pytest.mark.parametrize('_class', [*Card.__subclasses__()])
def test_card_class(user, _class):
    card = _class(user, Pos(1, 2))
    assert {
        'type': _class.__name__.lower(),
        'owner': user.id,
        'x': 1,
        'y': 2,
    } == card.serialize()


@pytest.mark.parametrize('_class', [*Card.__subclasses__()])
def test_load_card(user, _class):
    card = load_card({
        'type': _class.__name__.lower(),
        'owner': user.id,
        'x': 10,
        'y': 12,
    })
    assert isinstance(card, _class)
    assert card.owner == user
    assert card.pos == Pos(10, 12)
    card = load_card({
        'type': None,
        'owner': user.id,
        'x': 10,
        'y': 12,
    })
    assert card is None


@pytest.mark.parametrize('_class', [*Card.__subclasses__()])
def test_save_card(user, _class):
    card = _class(user, Pos(1, 2))
    assert card.serialize() == save_card(card)
