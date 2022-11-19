from datetime import datetime

import pytest

from pyAFL.base.exceptions import LookupError
from pyAFL.seasons.models import Season, SeasonStats


class TestSeasonModel:
    def test_season_none_throws_exception(self):
        with pytest.raises(TypeError):
            Season()

    def test_season_classmethod_get_season_url_success(self):
        assert (
            Season(2019)._get_season_url() == "https://afltables.com/afl/seas/2019.html"
        )

    def test_season_classmethod_get_season_url_failure(self):
        with pytest.raises(LookupError) as e:
            Season(12).get_season_stats()

        assert "Found no season for year" in str(e)

    def test_season_classmethod_get_season_stats(self):
        season = Season(2017)

        assert isinstance(season.get_season_stats(), SeasonStats)


class TestSeasonStats:
    season = Season(2017)
    stats = season.get_season_stats()
    matches = stats.season_matches
    # Match 54
    # St Kilda	                2.4   6.7  10.9 16.12	108
    # Greater Western Sydney	4.2   7.6 11.10 12.13	85
    # Fri 05-May-2017 7:50 PM Att: 21,160 Venue: Docklands
    # St Kilda won by 23 pts

    # Match 57
    # Port Adelaide	  2.3   5.7  7.13 12.15	87
    # West Coast	  4.1   7.3  12.4  15.7	97
    # Sat 06-May-2017 4:05 PM (4:35 PM) Att: 38,333 Venue: Adelaide Oval
    # West Coast won by 10 pts [Match stats]

    def test_season_match_parsing_home_team(self):
        assert self.matches[54].home_team == "St Kilda"

    def test_season_match_parsing_away_team(self):
        assert self.matches[54].away_team == "Greater Western Sydney"

    def test_season_match_parsing_time_AEST(self):
        assert self.matches[54].date == datetime.strptime(
            "05-May-2017 (7:50 pm)", "%d-%b-%Y (%I:%M %p)"
        )

    def test_season_match_parsing_time_not_AEST(self):
        assert self.matches[57].date == datetime.strptime(
            "06-May-2017 (4:35 pm)", "%d-%b-%Y (%I:%M %p)"
        )

    def test_season_match_home_team_score(self):
        assert self.matches[54].home_team_score == 108

    def test_season_match_result(self):
        # Important whitespace
        assert self.matches[54].result == "St Kilda  won by  23 pts"

    def test_season_match_margin(self):
        assert self.matches[54].margin == 23

    def test_match_repr(self):
        output = f"MATCH:\n\tPort Adelaide vs West Coast"
        output += f"\n\tRound: 7 game 4"
        output += f"\n\tVenue: Adelaide Oval"
        output += f"\n\tDate: 2017-05-06 16:35:00"
        output += f"\n\tHome team score: [2, 3, 5, 7, 7, 13, 12, 15]: 87"
        output += f"\n\tAway team score: [4, 1, 7, 3, 12, 4, 15, 7]: 97"
        output += f"\n\tResult: West Coast  won by  10 pts"
        output += f"\n\t(West Coast 10)\n"
        assert repr(self.matches[57]) == output

    def test_finals_match_repr(self):
        output = f"MATCH:\n\tGeelong vs Richmond (Qualifying Final)"
        output += f"\n\tRound: 25 game 1"
        output += f"\n\tVenue: M.C.G."
        output += f"\n\tDate: 2017-09-08 19:50:00"
        output += f"\n\tHome team score: [0, 4, 2, 4, 4, 9, 5, 10]: 40"
        output += f"\n\tAway team score: [2, 4, 3, 7, 6, 10, 13, 13]: 91"
        output += f"\n\tResult: Richmond  won by 51 pts"
        output += f"\n\t(Richmond 51)\n"
        assert repr(self.matches[199]) == output
