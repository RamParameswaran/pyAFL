import re
from datetime import datetime
from typing import Optional

import numpy as np
import pandas as pd

from pyAFL import config
from pyAFL.base.exceptions import LookupError
from pyAFL.session import session


class Season(object):
    """
    A class to represent an AFL season.

    Attributes
    ----------
    year : int
    stats : object
        MatchStats object

    Methods
    -------
    get_season_stats()
        Returns season stats objects, matches, matches_summary, ladders for each round, and a final ladder
    """

    def __init__(self, year: int, url: Optional[str] = None):
        """
        Constructs all the necessary attributes for the Season object.
         - If no season can be found for the given year, a
         `LookupError` exception is raised.

        Parameters
        ----------
            year : int (required)
                which year to get stats for
            url : str (optional)
                url to get stats from
        """

        self.season = year

        if url:
            self.url = url
        else:
            self.url = self._get_season_url()

    def __repr__(self):
        return f"<season: {self.season}>"

    def __str__(self):
        return str(self.season)

    def _get_season_url(self):
        return config.AFLTABLES_STATS_BASE_URL + f"seas/{self.season}.html"

    def get_season_stats(self, force_live=False):
        """
        Returns season stats as per the season stats page
        defined in `self._get_season_url()`

        Parameters
        ----------
            force_live : bool
                If True, does not use cached request

        Returns
        ----------
            stats : obj
                season stats Python object

        """

        resp = session.get(self.url, force_live)
        self._stat_html = resp.text

        try:
            all_dfs = pd.read_html(self._stat_html)
        except ValueError as exc:
            raise LookupError(
                f"Found no season for year {self.season}. Browse https://afltables.com/afl/seas/season_idx.html for a list of all years with data. Year must be an integer."
            ) from exc

        matches = []
        ladders = []
        final_ladder = []
        finals_stage = "Regular season"
        for df in all_dfs:
            # work out what data is in the table represented by this dataframe
            if df.iat[0, 0].startswith("Round"):
                # start of a round
                round = int(df.iat[0, 0].split(" ")[1])
                match = 1  # set to 1 as we're starting a new round
            elif df.shape[0] == 1:
                # Could be denoting which stage of finals, or could be a bye (which we ignore)
                if df.iat[0, 0].endswith("Final"):
                    finals_stage = df.iat[0, 0]
                    match = 1
                    round += 1
            else:
                # it's a match or a ladder
                if df.shape[0] > 1:
                    if df.iat[0, 0].startswith("Rd"):
                        # ladder tables start with Rd N
                        ladders.append(df)
                    elif isinstance(df.columns, pd.MultiIndex):
                        # it's the end-of-season ladder (drop last row of aggregate results which mess up the formatting)
                        final_ladder = df.head(-1)
                    else:
                        # it's a match
                        if not isinstance(df.iat[0, 1], str) and np.isnan(df.iat[0, 1]):
                            # if there are missing values it's because this season hasn't finished yet
                            final_ladder = []
                            break
                        # get the match object for this match
                        current_match = Match(df, round, match, finals_stage)
                        matches.append(current_match)
                        match += 1

        # build a summary dataframe of match data using the following column names and source variable names
        dataframe_fields = {
            "Date": "date",
            "Round": "round",
            "Game number": "game_number",
            "Venue": "venue",
            "Home team": "home_team",
            "Away Team": "away_team",
            "Home team score": "home_team_score",
            "Away team score": "away_team_score",
            "Home team score detail": "home_team_score_detail",
            "Away team score detail": "away_team_score_detail",
            "Winning team": "winning_team",
            "Margin": "margin",
            "Year stage": "finals_stage",
        }
        match_summary = {}
        for df_column_name, match_attribute_name in dataframe_fields.items():
            match_summary[df_column_name] = [
                getattr(match, match_attribute_name) for match in matches
            ]
        match_summary = pd.DataFrame(match_summary)

        ret = SeasonStats(
            season_matches=matches,
            season_ladders=ladders,
            final_ladder=final_ladder,
            match_summary=match_summary,
        )

        return ret


class SeasonStats(object):
    """
    A class to represent AFL season stats.

    Attributes
    ----------
    year : int
        season year
    stats : object
        SeasonStats object

    Methods
    -------
    ...
    """

    def __init__(self, **kwargs):
        """
        Constructs all the necessary attributes for the SeasonStats object.
         - kwargs passed are accessed as class attributes

        """

        super().__init__()
        self.__dict__.update(kwargs)
        pass


class Match:
    """
    A class to represent a match, extracting data from dataframe with match information from AFLtables

    Attributes
    ----------
    date : datetime
    round : int
    game_number : int
    venue : str
    result : str
    winning_team : str
    margin : int
    home_team : str
    away_team : str
    home_team_score : int
    away_team_score : int
    home_team_score_detail : List[int]
    away_team_score_detail : List[int]
    finals_stage : str

    Methods
    -------
    ...
    """

    def __init__(
        self,
        match: pd.DataFrame,
        round: int,
        game_number: int,
        finals_stage: str,
    ):
        """
        Constructs all the necessary attributes for the Match object.

        Parameters
        ----------
            match : DataFrame
                Match record from AFLTables
            round : int
                Round number in the season
            game_number : int
                Game number in the round
            finals_stage : str
                One of 'Regular season', 'Qualifying Final', 'Preliminary Final', 'Elimination Final', 'Grand Final'
        """
        # match is a dataframe that we have to extract data from, example:
        #             0                            1    2                                                                     3
        # 0  West Coast  0.0 Â Â 2.0 Â Â 4.3 Â Â 9.4   58  Fri 15-Apr-2022 5:40 PM (7:40 PM)  Att:  42,888 Venue: Perth Stadium
        # 1      Sydney        5.4 10.10 11.12 18.13  121          Sydney  won by  63 pts  [  Match stats  ]
        #
        # There are variations in the format...

        self.round = round
        self.game_number = game_number
        self.finals_stage = finals_stage
        self.date = self._parse_time(match)
        self.venue = match.iat[0, 3].split("Venue: ")[1].strip()
        self.result = match.iat[1, 3][:-18].strip()
        self.home_team = match.iat[0, 0]
        self.away_team = match.iat[1, 0]
        self.home_team_score = int(match.iat[0, 2])
        self.away_team_score = int(match.iat[1, 2])
        self.home_team_score_detail = self._score_detail(match.iat[0, 1])
        self.away_team_score_detail = self._score_detail(match.iat[1, 1])
        if self.home_team_score > self.away_team_score:
            self.winning_team = self.home_team
            self.margin = self.home_team_score - self.away_team_score
        elif self.home_team_score < self.away_team_score:
            self.winning_team = self.away_team
            self.margin = self.away_team_score - self.home_team_score
        else:
            self.winning_team = ""
            self.margin = 0

    def _parse_time(self, match):
        date_field = match.iat[0, 3].split(" ")
        # remove attendance field, it gets in the way
        if date_field[5] == "Att:":
            date_field = date_field[:4] + date_field[8:]

        # If local time is not AEST, AEST time appears in brackets, we pick AEST time
        if date_field[5].strip() == "Venue:":
            # local time is AEST
            match_date = " ".join(date_field[1:4])
            return datetime.strptime(match_date, "%d-%b-%Y %I:%M %p")
        else:
            match_date = " ".join(date_field[1:2] + date_field[4:6])
            return datetime.strptime(match_date, "%d-%b-%Y (%I:%M %p)")

    def _score_detail(self, score):
        # Score is a string like '0.0 Â Â 2.0 Â Â 4.3 Â Â 9.4' and there are weird characters
        # Get the relevant ones with a regex, then split on decimals to split goals/behinds
        strings = [x.split(".") for x in re.findall("\\d*\\.?\\d+", score)]
        return [int(y) for x in strings for y in x]

    def __repr__(self):
        output = f"MATCH:\n\t{self.home_team} vs {self.away_team}"
        if self.finals_stage != "Regular season":
            output += f" ({self.finals_stage})"
        output += f"\n\tRound: {self.round} game {self.game_number}"
        output += f"\n\tVenue: {self.venue}"
        output += f"\n\tDate: {self.date}"
        output += f"\n\tHome team score: {self.home_team_score_detail}: {self.home_team_score}"
        output += f"\n\tAway team score: {self.away_team_score_detail}: {self.away_team_score}"
        output += f"\n\tResult: {self.result}"
        output += f"\n\t({self.winning_team} {self.margin})\n"
        return output
