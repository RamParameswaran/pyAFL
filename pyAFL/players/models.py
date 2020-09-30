from bs4 import BeautifulSoup
import re
import requests

from pyAFL import config
from pyAFL.base.exceptions import LookupError
from pyAFL.base.models import AFLObject


class Player(AFLObject):
    """
    A class to represent an AFL player.

    Attributes
    ----------
    name : str
        first name of the person
    stats : object
        PlayerStats object

    Methods
    -------
    ...
    """

    def __init__(self, name: str, team: str = None):
        """
        Constructs all the necessary attributes for the Player object.
         - If the player does not exist in the local DB, a search will
         be performed.
         - If `name` returns two or more players, the (optional) parameter
         "team" is used to select the correct player.
         - If no player can be found for the given "name", "team"
         combination, a `LookupError` exception is raised.

        Parameters
        ----------
            name : str (required)
                name of the person in format "[first] [last]"
            team : str (string)
                name of team that the player has played in during their career
        """

        if self._get_object_from_db(name=name, team=team):
            self = self._get_object_from_db(name=name, team=team)
            return

        self.name = name.title()  # Convert to title case for URL string matching
        self.team = (
            team.title() if team else None
        )  # Convert to title case for URL string matching
        self.url = self._get_player_url()

    def _get_player_url(self):
        last_initial = self.name.split(" ")[1][0]
        player_list_url = (
            config.AFLTABLES_STATS_BASE_URL + f"players{last_initial}_idx.html"
        )

        resp = requests.get(player_list_url)
        soup = BeautifulSoup(resp.text, "html.parser")

        url_list = soup.findAll(
            "a",
            href=re.compile(f"^players/{self.name[0]}/{self.name.replace(' ', '_')}"),
        )

        # If no matches found, raise LookupError
        if len(url_list) == 0:
            raise LookupError(
                f"Found no players with name {self.name}. Browse https://afltables.com/afl/stats/playersA_idx.html for a list of all players. Name must be in format '[first] [last]'."
            )

        # If more than one name is matched, print warning message and return first.
        if len(url_list) > 1:
            print(
                f"Warning: {len(url_list)} players have been found for name: {self.name}. Returning only the first"
            )

        return config.AFLTABLES_STATS_BASE_URL + url_list[0].attrs.get("href")
