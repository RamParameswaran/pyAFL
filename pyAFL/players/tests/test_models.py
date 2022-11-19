import pytest

from pyAFL.base.exceptions import LookupError
from pyAFL.players.models import Player, PlayerStats


class TestPlayerModel:
    def test_player_name_none_throws_exception(self):
        with pytest.raises(TypeError):
            Player()

    def test_player_classmethod_get_player_url_success(self):
        assert (
            Player("Nathan Brown")._get_player_url() ==
            "https://afltables.com/afl/stats/players/N/Nathan_Brown0.html"
        )
        assert (
            Player("Nick Riewoldt")._get_player_url() ==
            "https://afltables.com/afl/stats/players/N/Nick_Riewoldt.html"
        )
        assert (
            Player("Tony Lockett")._get_player_url() ==
            "https://afltables.com/afl/stats/players/T/Tony_Lockett.html"
        )
        assert (
            Player("Duncan MacGregor")._get_player_url() ==
            "https://afltables.com/afl/stats/players/D/Duncan_MacGregor.html"
        )

    def test_player_classmethod_get_player_url_failure(self):
        with pytest.raises(LookupError) as e:
            Player("Babe Ruth")._get_player_url()

        assert "Found no players with name" in str(e)

    def test_player_classmethod_get_player_stats(self):
        player = Player("Nick Riewoldt")

        assert isinstance(player.get_player_stats(), PlayerStats)
