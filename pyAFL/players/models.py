import re

import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from pyAFL import config
from pyAFL.base.exceptions import LookupError
from pyAFL.session import session


class Player(object):
    """
    A class to represent an AFL player.

    Attributes
    ----------
    name : str
        first name of the person
    url : str
        url to the player's information page
    metadata : dictionary
        player bio information 

    Methods
    -------
    get_player_stats : returns PlayerStats object
    ...
    """

    def __init__(self, name: str, url: str = None, team: str = None):
        """
        Constructs all the necessary attributes for the Player object.
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

        self.name = name.title()  # Convert to title case for URL string matching
        self.name = self.name.replace("\n", "").strip()
        self.metadata = {}
        if url:
            self.url = url
        else:
            self.url = self._get_player_url()

    def __repr__(self):
        return f"<Player: {self.name}>"

    def __str__(self):
        return self.name

    def _get_player_url(self):
        last_initial = self.name.split(" ")[1][0]
        player_list_url = (
            config.AFLTABLES_STATS_BASE_URL + f"stats/players{last_initial}_idx.html"
        )

        resp = session.get(player_list_url)
        soup = BeautifulSoup(resp.text, "html.parser")

        url_list = soup.findAll(
            "a",
            href=re.compile(
                f"players/{self.name[0]}/{self.name.replace(' ', '_')}", re.I
            ),
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

        return url_list[0].attrs.get("href")
    
    def _get_bio_info(self, b_tags):
        for bio in b_tags:
            if re.sub(r"[\n\t\s]*", "", bio.get_text())=="Born:":
                date_born = re.sub(r"[\n\t\s]*", "", bio.next_sibling.replace(" (",""))
                timestamp = datetime.strptime(date_born, '%d-%b-%Y').strftime('%d-%b-%Y')
                self.metadata["born"] = timestamp
            if re.sub(r"[\n\t\s]*", "", bio.get_text())=="Debut:":
                debut = bio.next_sibling.strip().split(" ") # Ex:18y 218d
                timestamp = (datetime.strptime(self.metadata["born"], '%d-%b-%Y') + timedelta(int(debut[0][:-1]) * 365 + int(debut[1][:-1]))).strftime('%d-%b-%Y')
                print("debut:", timestamp)
                self.metadata["debut"] = timestamp
            if re.sub(r"[\n\t\s]*", "", bio.get_text())=="Last:":
                last = bio.next_sibling.replace(")","").strip().split(" ")
                timestamp = (datetime.strptime(self.metadata["born"], '%d-%b-%Y') + timedelta(int(last[0][:-1]) * 365 + int(last[1][:-1]))).strftime('%d-%b-%Y')
                print("last:", timestamp)
                self.metadata["last"] = timestamp
            if re.sub(r"[\n\t\s]*", "", bio.get_text())=="Height:":
                self.metadata["height"] = re.sub("[^0-9]", "",bio.next_sibling)
            if re.sub(r"[\n\t\s]*", "", bio.get_text())=="Weight:":
                self.metadata["weight"] = re.sub("[^0-9]", "",bio.next_sibling)

    def get_player_stats(self):
        """
        Returns player stats as per the player stats page defined in `self._get_player_url()`

        Returns
        ----------
            stats : obj
                player stats Python object

        """

        resp = session.get(self.url)
        self._stat_html = resp.text

        soup = BeautifulSoup(self._stat_html, "html.parser")

        self._get_bio_info(soup.find_all('b'))

        all_dfs = pd.read_html(self._stat_html)
        season_dfs = pd.read_html(self._stat_html, match=r"[A-Za-z]* - [0-9]{4}")

        season_stats_total = all_dfs[0]  # The first table on the page
        season_stats_average = all_dfs[1]  # The second table on the page

        ret = PlayerStats(
            season_stats_total=season_stats_total,
            season_stats_average=season_stats_average,
            season_results=season_dfs,
        )

        return ret


class PlayerStats(object):
    """
    A class to represent an AFL player.

    Attributes
    ----------
    season_stats_total : object
    season_stats_average : object
    season_results : object

    Methods
    -------
    ...
    """

    def __init__(self, **kwargs):
        """
        Constructs all the necessary attributes for the PlayerStats object.
         - kwargs passed are accessed as class attributes

        """

        super().__init__()
        self.__dict__.update(kwargs)
        pass
