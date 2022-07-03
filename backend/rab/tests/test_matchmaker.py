import asyncio

import pytest


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
    matchmaker.users_queue = users_queue
    oponent = matchmaker.get_oponent(user)
    assert oponent == expected


async def test_matchmaker(matchmaker):
    async def user_session(user, oponent, search_after=0):
        await asyncio.sleep(search_after)
        matchmaker.enter_queue(user)

        found_oponent = await matchmaker.searcher(user)
        assert found_oponent == oponent

    task1 = asyncio.create_task(user_session('user1', 'user2'))
    task2 = asyncio.create_task(user_session('user2', 'user1'))

    await task1
    await task2

    assert matchmaker.users_queue == []
