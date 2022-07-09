import asyncio

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


async def test_matchmaker(matchmaker):
    boards = {}

    async def user_session(user, oponent):
        found_oponent = await matchmaker.search_oponent(user)
        assert found_oponent == oponent
        boards[user] = await matchmaker.build_board(user, oponent, board_builder_mock)

    task1 = asyncio.create_task(user_session('user1', 'user2'))
    task2 = asyncio.create_task(user_session('user2', 'user1'))

    await task1
    await task2

    assert matchmaker.mmqueue.queue == []
    assert boards['user1'] == boards['user2']


async def test_matchmaking_api(
        auth_client_with,
        user1,
        user2,
        monkeypatch,
        matchmaker,
        db_session,
):
    monkeypatch.setattr('rab.main.lock', asyncio.Lock())
    db_session.add(user1)
    db_session.add(user2)
    await db_session.commit()

    async with (
            auth_client_with(user1).websocket_connect('/game/search') as client1,
            auth_client_with(user2).websocket_connect('/game/search') as client2,
    ):
        ...
        resp1 = await client1.receive_json()
        resp2 = await client2.receive_json()
        assert resp1 == resp2
