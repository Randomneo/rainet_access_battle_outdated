from core.board_manager import BoardManager
from core.cards import Pos
from core.cards import load_card
from core.models import Board


def test_board_manager(user):
    board = Board.load(user, None, [
        ['p1virus', 'p1link', 'link', 'virus'],
        ['_', '_', '_', '_'],
        ['_', '_', '_', '_'],
    ])
    assert isinstance(board.manager, BoardManager)
    assert len(board.manager.board) == 4
    assert board.manager.get_by_pos(Pos(1, 1)) is None
    assert board.manager.get_by_pos(Pos(0, 0))
    board.manager.move(Pos(0, 0), Pos(1, 1))
    assert board.manager.get_by_pos(Pos(1, 1))
    assert board.manager.get_by_pos(Pos(0, 0)) is None
    assert len(board.manager.user_cards(user)) == 2
    assert len(board.manager.user_cards(None)) == 2


def test_board_load(user):
    board = BoardManager.load(user, None, [['virus', 'link', '_']])
    assert len(board) == 2, board


def test_board_add(user):
    board = Board.load(user, None, [
        ['p1virus', 'p1link', 'link', 'virus'],
        ['_', '_', '_', '_'],
        ['_', 'exit', '_', '_'],
    ])
    assert not any(filter(lambda x: x.pos == Pos(3, 3), board.manager.board))
    board.manager.add(load_card({
        'type': 'link',
        'owner': user.id,
        'x': 3,
        'y': 3,
    }))
    assert any(filter(lambda x: x.pos == Pos(3, 3), board.manager.board))


def test_exit_layout(user):
    board = Board.load(user, None, [[]])
    board.manager.exit_layout()
    assert len(board.manager.board) == 4
