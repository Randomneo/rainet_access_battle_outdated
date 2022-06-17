import pytest

from ..board_manager import BoardManager
from ..board_manager import NoWinner
from ..cards import Link
from ..cards import Pos
from ..cards import Virus
from ..cards import load_card
from ..models import Board


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
    board.manager.pprint()
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
        'owner': user,
        'x': 3,
        'y': 3,
    }))
    assert any(filter(lambda x: x.pos == Pos(3, 3), board.manager.board))


def test_exit_layout(user):
    board = Board.load(user, None, [[]])
    board.manager.exit_layout()
    assert len(board.manager.board) == 4


def test_stack(user):
    board = Board.load(user, None, [[]])
    assert len(board.manager.user_stack(user)) == 0
    board.manager.add_stack(user, load_card({
        'type': 'link',
        'owner': user,
        'x': 3,
        'y': 3,
    }))
    board.manager.add_stack(None, load_card({
        'type': 'virus',
        'owner': user,
        'x': 3,
        'y': 3,
    }))
    assert len(board.manager.user_stack(user)) == 1
    assert len(board.manager.user_stack(None)) == 1


def test_exception_add_stack(user):
    with pytest.raises(KeyError):
        Board.load(None, None, [[]]).manager.user_stack(user)


@pytest.mark.parametrize('p1_stack, p2_stack, is_p1_winner', [
    (
        [Virus(None, Pos(0, 0))]*3,
        [Link(None, Pos(0, 0))]*3,
        None,
    ),
    (
        [Virus(None, Pos(0, 0))]*4,
        [Link(None, Pos(0, 0))]*3,
        False,
    ),
    (
        [Link(None, Pos(0, 0))]*4,
        [Link(None, Pos(0, 0))]*3,
        True,
    ),
    (
        [Virus(None, Pos(0, 0))]*3,
        [Virus(None, Pos(0, 0))]*4,
        True,
    ),
    (
        [Virus(None, Pos(0, 0))]*3,
        [Link(None, Pos(0, 0))]*4,
        False,
    ),
    # not possible but in case
    # expected: decide by second player decision
    (
        [Virus(None, Pos(0, 0))]*4,
        [Virus(None, Pos(0, 0))]*4,
        True,
    ),
    (
        [Link(None, Pos(0, 0))]*4,
        [Link(None, Pos(0, 0))]*4,
        False,
    ),
])
def test_decide_winner(user, p1_stack, p2_stack, is_p1_winner):
    user2 = 'user2'
    board = Board.load(user, user2, [[]])
    board.manager.player1_stack = p1_stack
    board.manager.player2_stack = p2_stack

    if is_p1_winner:
        assert board.manager.decide_winner() == user
    elif is_p1_winner is False:
        assert board.manager.decide_winner() == user2
    else:
        with pytest.raises(NoWinner):
            board.manager.decide_winner()
