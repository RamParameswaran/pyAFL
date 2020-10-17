from bs4 import BeautifulSoup

from pyAFL.players.models import Player
from pyAFL.requests import requests


class Team(object):
    """
    A class to represent an AFL Team.

    Attributes
    ----------
    name : str
        team full name
    players : object
        list of all time players who played for the team (pyAFL player objects)

    """

    def __init__(self, name: str, url_identifier: str):
        """
        Constructs the Team object.

        Parameters
        ----------
            name : str (required)
                name of the person in format "[first] [last]"
            url_identifier : str (required)
                string parameter used in AFLtables URLs to identify team. Note that the naming convention changes from team to team
                Examples: - for Adelaide: url_identifier = "adelaide" (see https://afltables.com/afl/stats/teams/adelaide.html)
                          - for Greater Western Sydney: url_identifier = "gws" (see https://afltables.com/afl/stats/teams/gws.html)
                          - for Western Bulldogs: url_identifier = "bullldogs" (see https://afltables.com/afl/stats/teams/bullldogs.html)

        """

        self.name = name.title()  # Convert to title case for URL string matching
        self.all_time_players_url = f"https://afltables.com/afl/stats/teams/{url_identifier}.html"  # URL for all-time-players stats
        self.all_time_games_url = f"https://afltables.com/afl/teams/{url_identifier}/allgames.html"  # URL to all-time-games stats

    @property
    def players(self):
        """
        NB - a network request will be made when this class property is called.
        """

        return self._get_players()

    def _get_players(self):
        """
        Returns a list of pyAFL.Player objects for all players contained in `self.all_time_players_url`

        Returns
        ----------
            players : list
                list of pyAFL.Player objects

        """
        resp = requests.get(self.all_time_players_url)
        soup = BeautifulSoup(resp.text, "html.parser")

        player_table = soup.find("table")
        player_table_body = player_table.find("tbody")
        player_anchor_tags = player_table_body.findAll("a")

        players = [
            Player(player.text, url=player.attrs.get("href"))
            for player in player_anchor_tags
        ]

        return players

