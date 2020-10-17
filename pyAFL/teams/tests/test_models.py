import pandas as pd
import pytest
from unittest import mock

from pyAFL.base.exceptions import LookupError
from pyAFL.players.models import Player
from pyAFL.teams.models import Team
from pyAFL.requests import requests


class TestTeamModel:
    def test_team_name_none_throws_exception(self):
        with pytest.raises(TypeError):
            Team()

    def test_team_property_players(self):
        from pyAFL.teams import ALL_TEAMS

        test_team = ALL_TEAMS[0]
        players = test_team.players

        assert isinstance(players, (list, tuple))
        assert len(players) > 0
        assert isinstance(players[0], Player)
        assert "https://afltables.com/afl/stats/players" in players[0].url

    def test_team_method_season_stats_invalid_year(self):
        from pyAFL.teams import ALL_TEAMS

        test_team = ALL_TEAMS[0]
        with pytest.raises(Exception) as e1:
            test_team.season_stats(123)
        with pytest.raises(Exception) as e2:
            test_team.season_stats(2050)

        assert "Could not find season stats for year" in str(e1)
        assert "Could not find season stats for year" in str(e2)

    def test_team_method_season_stats_valid_year(self):
        from pyAFL.teams import CURRENT_TEAMS

        test_team = CURRENT_TEAMS[0]
        season_stats = test_team.season_stats(2019)

        assert isinstance(season_stats, pd.DataFrame)
        assert "Player" in season_stats.columns
