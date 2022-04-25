import pytest
from unittest import mock

from pyAFL.base.exceptions import LookupError
from pyAFL.seasons.models import Season, SeasonStats
from pyAFL.requests import requests


class TestSeasonModel:
    def test_season_none_throws_exception(self):
        with pytest.raises(TypeError):
            Season()

    def test_season_classmethod_get_season_url_success(self):
        assert (
            Season(2019)._get_season_url()
            == "https://afltables.com/afl/seas/2019.html"
        )

    def test_season_classmethod_get_season_url_failure(self):
        with pytest.raises(LookupError) as e:
            Season(12).get_season_stats()

        assert "Found no season for year" in str(e)

    def test_season_classmethod_get_season_stats(self):
        season = Season(2017)

        assert isinstance(season.get_season_stats(), SeasonStats)
