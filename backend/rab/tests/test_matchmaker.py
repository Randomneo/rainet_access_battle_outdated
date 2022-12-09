import pytest


async def board_builder_mock(player1, player2):
    class MockBoardBuilder:
        def __init__(self, player1, player2):
            self.player1 = player1
            self.player2 = player2
    return MockBoardBuilder(player1, player2)


@pytest.mark.parametrize('user, users_queue, expected', [
    [
        'user1',
        ['user1', 'user2', 'user3'],
        'user2',
    ],
    [
        'user2',
        ['user1', 'user2', 'user3'],
        'user1',
    ],
    [
        'user2',
        ['user1', 'user2'],
        'user1',
    ],
    [
        'user1',
        ['user1', 'user2'],
        'user2',
    ],
    [
        'user1',
        ['user1'],
        None,
    ],
])
def test_get_oponent(user, users_queue, expected, matchmaker):
    matchmaker.mmqueue.queue = users_queue
    oponent = matchmaker.mmqueue.get_oponent(user)
    assert oponent == expected
