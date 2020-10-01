import pytest
from unittest import mock

from pyAFL.base.exceptions import LookupError
from pyAFL.players.models import Player
from pyAFL.requests import requests


@pytest.fixture(scope="session")
def test_html_cache_path(tmpdir_factory):
    fn = tmpdir_factory.mktemp("__HTMLCACHE__")
    return fn


class TestPlayerModel:
    @pytest.fixture
    def mock_html_cache_dir(self, monkeypatch, test_html_cache_path):
        monkeypatch.setattr(requests, "get_html_cache_path", mock.Mock())
        requests.get_html_cache_path.return_value = str(test_html_cache_path)

    def test_player_name_none_throws_exception(self):
        with pytest.raises(TypeError):
            Player()

    def test_player_classmethod_get_player_url_success(self, mock_html_cache_dir):
        assert (
            Player("Nathan Brown")._get_player_url()
            == "https://afltables.com/afl/stats/players/N/Nathan_Brown0.html"
        )
        assert (
            Player("Nick Riewoldt")._get_player_url()
            == "https://afltables.com/afl/stats/players/N/Nick_Riewoldt.html"
        )
        assert (
            Player("Tony Lockett")._get_player_url()
            == "https://afltables.com/afl/stats/players/T/Tony_Lockett.html"
        )
        assert (
            Player("Tony Lockett")._get_player_url()
            == "https://afltables.com/afl/stats/players/T/Tony_Lockett.html"
        )

    def test_player_classmethod_get_player_url_failure(self, mock_html_cache_dir):
        with pytest.raises(LookupError) as e:
            Player("Babe Ruth")._get_player_url()

        assert "Found no players with name" in str(e)
