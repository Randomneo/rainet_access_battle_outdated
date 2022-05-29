import pytest

from core.gameorchestrator import ActionError
from core.gameorchestrator import SetLayoutAction


@pytest.mark.parametrize('i,j,field,expected', [
    (7, 7, 'virus', (1, 0)),
    (6, 7, 'virus', ActionError),
    (6, 4, 'virus', (1, 0)),
    (7, 7, 'link', (0, 1)),
    (6, 7, 'link', ActionError),
    (6, 4, 'link', (0, 1)),
    (1, 1, '_', (0, 0)),
])
def test_validate_field(i, j, field, expected):
    if expected == ActionError:
        with pytest.raises(expected):
            SetLayoutAction.validate_field(i, j, field)
    else:
        assert expected == SetLayoutAction.validate_field(i, j, field)


@pytest.mark.parametrize('board,expected', [
    ([
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', 'virus', 'link', '', '', ''],
        ['virus', 'virus', 'virus', '', '', 'link', 'link', 'link'],
    ], None),
    ([
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', 'virus', 'link', '', '', ''],
        ['virus', 'virus', '', '', '', 'link', 'link', 'link'],
    ], ActionError),
    ([
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', 'virus', 'link', '', '', ''],
        ['virus', 'virus', 'virus', '', '', '', 'link', 'link'],
    ], ActionError),
    ([
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['virus', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', 'virus', 'link', '', '', ''],
        ['virus', 'virus', '', '', '', '', 'link', 'link'],
    ], ActionError),
])
def test_validate_board(board, expected):
    if expected == ActionError:
        with pytest.raises(expected):
            SetLayoutAction.validate_board(board)
    else:
        SetLayoutAction.validate_board(board)
