import pytest

from bs4 import BeautifulSoup
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

        player = Player("Stuart Magee")
        player.get_player_stats()

        assert(player.metadata["born"] == "13-Oct-1943")
        assert(player.metadata["debut"] == "14-May-1962")
        assert(player.metadata["last"] == "22-Aug-1975")

    def test_unvavailable_player_bio(self):
        # Mock an empty, or None value
        # Case: date of birth is unavailable but debut or last is/are,
        #       player.metadata['debut' and 'last'] = None
        player = Player("Nathan Brown")

        html_content = """
            <html>
            <body>
                <center>
                    <b>Born:</b>
                     (
                    <b>Debut:</b>
                    18y 218d
                    <b>Last:</b>
                    )
                    <b>Height:</b>

                    <b>Weight:</b>
                    74 kg
                </center>
            </body>
            </html>
        """

        soup = BeautifulSoup(html_content, 'html.parser')

        player._get_bio_info(soup.find_all('b'))
        
        print("player.metadata:", player.metadata)

        assert(player.metadata["born"] == None)
        assert(player.metadata["debut"] == None)
        assert(player.metadata["height"] == None)
        assert(player.metadata["weight"] == "74")
        assert(player.metadata["last"] == None)
