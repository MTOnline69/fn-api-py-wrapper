import datetime
from typing import Any
import pytest
import os

import fortnite_api

TEST_STAT_ACCOUNT_NAME = "Luc1412"
TEST_STAT_ACCOUNT_ID = '369644c6224d4845aa2b00e63b60241d'


# This is a module-scoped fixture, meaning it will only be called once for the entire module
@pytest.fixture(scope='module')
def api_key():
    gh_actions = os.environ.get('GITHUB_ACTIONS')
    if gh_actions and gh_actions == 'true':
        return os.environ['TEST_API_KEY']

    # This is a local development environment, try and load a .env file and get the API key
    from dotenv import load_dotenv

    load_dotenv()
    return os.environ['TEST_API_KEY']


def _test_stats(player_stats: fortnite_api.BrPlayerStats[Any]) -> None:
    assert player_stats.user

    if player_stats.battle_pass:
        assert player_stats.battle_pass.level
        assert player_stats.battle_pass.progress

    stats = player_stats.stats
    overall_stats = stats and stats.all and stats.all.overall
    if not overall_stats:
        # Nothing we should be testing
        return

    assert isinstance(overall_stats, fortnite_api.BrGameModeStats)
    assert isinstance(overall_stats.score, int)
    assert isinstance(overall_stats.score_per_min, float)
    assert isinstance(overall_stats.score_per_match, float)
    assert isinstance(overall_stats.wins, int)

    # This is overall stats, so these topX should all be not None
    assert isinstance(overall_stats.top3, int)
    assert isinstance(overall_stats.top5, int)
    assert isinstance(overall_stats.top6, int)
    assert isinstance(overall_stats.top10, int)
    assert isinstance(overall_stats.top12, int)
    assert isinstance(overall_stats.top25, int)

    assert isinstance(overall_stats.kills, int)
    assert isinstance(overall_stats.kills_per_min, float)
    assert isinstance(overall_stats.kills_per_match, float)

    assert isinstance(overall_stats.deaths, int)
    assert isinstance(overall_stats.kd, float)
    assert isinstance(overall_stats.win_rate, float)
    assert isinstance(overall_stats.minutes_played, int)
    assert isinstance(overall_stats.players_outlived, int)
    assert isinstance(overall_stats.last_modified, datetime.datetime)


@pytest.mark.asyncio
async def test_async_fetch_br_stats(api_key: str):
    async with fortnite_api.FortniteAPI(api_key=api_key) as client:
        stats = await client.fetch_br_stats(TEST_STAT_ACCOUNT_NAME, image=fortnite_api.StatsImageType.ALL)

    assert stats is not None
    _test_stats(stats)


def test_sync_fetch_br_stats(api_key: str):
    with fortnite_api.SyncFortniteAPI(api_key=api_key) as client:
        stats = client.fetch_br_stats(TEST_STAT_ACCOUNT_NAME, image=fortnite_api.StatsImageType.ALL)

    assert stats is not None
    _test_stats(stats)
