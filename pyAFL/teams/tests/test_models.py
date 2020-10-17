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