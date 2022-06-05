from dataclasses import dataclass

from django.contrib.auth import get_user_model

User = get_user_model()


@dataclass
class Pos:
    x: int
    y: int


class Card:
    def __init__(self, owner: User, pos: Pos):
        self.type = self.__class__.__name__.lower()
        self.owner = owner
        self.pos = pos

    def serialize(self):
        return {
            'type': self.type,
            'owner': getattr(self.owner, 'id', None),
            'x': self.pos.x,
            'y': self.pos.y,
        }

    @classmethod
    def deserialize(cls, data: dict):
        return cls(
            User.objects.filter(id=data['owner']).first(),
            Pos(x=data['x'], y=data['y'])
        )

    def __repr__(self):
        return f'{self.__class__.__name__} Pos({self.pos.x}, {self.pos.y}) o={self.owner}'


class Virus(Card):
    ...


class Link(Card):
    ...


class Exit(Card):
    ...


def type_to_card(type: str):
    return {card.__name__.lower(): card for card in Card.__subclasses__()}[type]


def save_card(card: Card):
    return card.serialize()


def load_card(data: dict):
    try:
        return type_to_card(data['type']).deserialize(data)
    except KeyError:
        return None
