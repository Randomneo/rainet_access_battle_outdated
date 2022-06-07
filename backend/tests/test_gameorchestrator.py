from core.gameorchestrator import MoveAction
from core.gameorchestrator import SetLayoutAction
from core.models import Board


def test_setlayoutaction(socket, monkeypatch):
    monkeypatch.setattr('core.validators.SetLayoutValidator.validate', lambda self, x: None)

    SetLayoutAction(socket).load([[]]).act()
    assert Board.objects.all().count() == 1


def test_moveaction(socket, monkeypatch):
    monkeypatch.setattr('core.ai.choice', lambda x: x[0])

    Board.load(socket.scope['user'], None, [['virus', 'link']])
    action = MoveAction(socket).load({
        'from': {'x': 0, 'y': 0},
        'to': {'x': 0, 'y': 1},
    }).act()
    assert len(socket.sent) == 0
    assert action == {
        'type': 'move enemy',
        'data': {
            'from': [0, 1],
            'to': [0, 0],
        },
    }
