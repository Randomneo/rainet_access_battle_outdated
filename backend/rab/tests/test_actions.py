import pytest

from ..validators import ActionValidationError
from ..validators import SetLayoutValidator


@pytest.mark.parametrize('i,j,field,expected', [
    (7, 7, 'virus', (1, 0)),
    (6, 7, 'virus', ActionValidationError),
    (6, 4, 'virus', (1, 0)),
    (7, 7, 'link', (0, 1)),
    (6, 7, 'link', ActionValidationError),
    (6, 4, 'link', (0, 1)),
    (1, 1, '_', (0, 0)),
])
def test_validate_field(i, j, field, expected):
    if expected == ActionValidationError:
        with pytest.raises(expected):
            SetLayoutValidator().validate_field(i, j, field)
    else:
        assert expected == SetLayoutValidator().validate_field(i, j, field)


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
    ], ActionValidationError),
    ([
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', 'virus', 'link', '', '', ''],
        ['virus', 'virus', 'virus', '', '', '', 'link', 'link'],
    ], ActionValidationError),
    ([
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['virus', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', 'virus', 'link', '', '', ''],
        ['virus', 'virus', '', '', '', '', 'link', 'link'],
    ], ActionValidationError),
])
def test_validate_board(board, expected):
    if expected == ActionValidationError:
        with pytest.raises(expected):
            SetLayoutValidator().validate(board)
    else:
        SetLayoutValidator().validate(board)
