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

        player1 = Player("Stuart Magee")
        player1.get_player_stats()
        assert(player1.metadata["born"] == "13-Oct-1943")
        assert(player1.metadata["debut"] == "14-May-1962") # afltables: first game was May 19
        assert(player1.metadata["last"] == "22-Aug-1975") # afltables: last game was August 23


        assert isinstance(player.get_player_stats(), PlayerStats)
