![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)
[![PyPI Latest Release](https://img.shields.io/pypi/v/pyAFL.svg)](https://pypi.org/project/pyAFL/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pandas)
![Build and Test](https://github.com/RamParameswaran/pyAFL/workflows/Build%20and%20Test/badge.svg)

<p align="center">
     <img src="/static/img/AFL-logo.png" width="540" height="360">
</p>

# pyAFL

pyAFL is a AFL (Australian Football League) data fetching libary. It scrapes data from https://afltables.com/ and converts results to structured Python objects for easier analytics.


## Installation

1. Install from pyPI
   `pip install pyAFL`

**OR**

2. Clone the repository locally:
   `git clone https://github.com/RamParameswaran/pyAFL.git`


## API

- Player
  - [Player()](#Player)
  - [Player.get_player_stats()](#Player.get_player_stats)
- Team
  - [Team()](#Team)
  - [Team.players](#Team.players)
  - [Team.games](#Team.games)
  - [Team.season_stats(year)](#Team.season_stats)
- Season
  - [Season()](#Season)
  - [Season.get_season_stats()](#Season.get_season_stats)

### Player()

Instantiates the Player object. The **init** method finds the matching player on afltables.com based on the `name` argument string. `name` must be an exact match, in the format "Firstname Lastname" and must be a name listed at https://afltables.com/afl/stats/playersA_idx.html

### Player.get_player_stats()

Pulls player stats (career totals, and season-by-season summary) and presents as a Python object.
This function returns a PlayerStats object with attributes:

- season_stats_total (Pandas dataframe)
- season_stats_average (Pandas dataframe)
- season_results (list of Pandas dataframes)

**Example**

    >>> from pyAFL.players.models import Player

    >>> player = Player("Nick Riewoldt")
    >>> player.url
    "https://afltables.com/afl/stats/players/N/Nick_Riewoldt.html"

    >>> stats = player.get_player_stats()
    >>> stats.season_stats_total
                Year      Team         #      GM  ...       MI      1%     BO      GA
        0       2001  St Kilda        12    6.00  ...     2.00    2.00   2.00     NaN
        1       2002  St Kilda        12   22.00  ...    28.00   44.00  13.00     NaN
        2       2003  St Kilda        12   22.00  ...    39.00   38.00  11.00    5.00
        3       2004  St Kilda        12   25.00  ...    89.00   46.00   7.00   27.00

    >>> stats.season_stats_average
                Year      Team         #      GM  ...       MI      1%     BO      GA
        0       2001  St Kilda        12    6.00  ...     0.33    0.33   0.33     NaN
        1       2002  St Kilda        12   22.00  ...     1.27    2.00   0.59     NaN
        2       2003  St Kilda        12   22.00  ...     1.77    1.73   0.50    0.23
        3       2004  St Kilda        12   25.00  ...     3.56    1.84   0.28    1.08

    >>> stats.season_results
        [  St Kilda - 2001   ...8 columns],    St Kilda - 2002  ...8 columns],    St Kilda - 2003  ...8 columns],    St Kilda - 2004  ...8 columns],    St Kilda - 2005  ...8 columns],    St Kilda - 2006  ...8 columns], ...]

### Team()

Instantiates a Team object. pyAFL automatically instantiates Team objects for all current and former AFL teams. They can be imported by their team abbreviation:

    >>> from pyAFL.teams import (ADE, BRI, BRB, CAR, COL, ESS, FIZ, FRE, GEE, GC, GWS, HAW, MEL, NOR, POR, RIC, STK, SYD, UNI, WCE, WBD)
    >>> # or
    >>> from pyAFL.teams import ALL_TEAMS, CURRENT_TEAMS

    >>> ADE
        <Team: Adelaide>

    >>> CURRENT_TEAMS
        [<Team: Adelaide>, <Team: Brisbane Lions>, <Team: Carlton>, <Team: Collingwood>, <Team: Essendon>, <Team: Fremantle>, <Team: Geelong>, <Team: Gold Coast>, <Team: Greater Western Sydney>, <Team: Hawthorn>, <Team: Melbourne>, <Team: North Melbourne>, <Team: Port Adelaide>, <Team: Richmond>, ...]

### Team.players

Returns a list of all historical players for this team. The return is a list of pyAFL [Player](#Player) objects. These Player objects can be queried to get player stats using the Player classmethods noted above.

    >>> from pyAFL.teams import ADE

    >>> # Let's get a list of all players who have every played for Adelaide (i.e. all players from https://afltables.com/afl/stats/teams/adelaide.html)
    >>> ADE.players
        [<Player: Mcleod, Andrew>, <Player: Edwards, Tyson>, <Player: Ricciuto, Mark>, <Player: Hart, Ben>, <Player: Smart, Nigel>, <Player: Goodwin, Simon>, <Player: Bickley, Mark>, <Player: Thompson, Scott>, ...]

### Team.games

Returns a Pandas DataFrame with all historical game results for this team. The DataFrame has a datetime index.

    >>> from pyAFL.teams import ADE

    >>> # Let's get all historical game data (i.e. all the data from https://afltables.com/afl/teams/adelaide/allgames.html)
    >>> ADE.games
                             Rnd  T  ...    Crowd                      Date
        Date                         ...
        1991-03-22 19:40:00   R1  H  ...  44902.0   Fri 22-Mar-1991 7:40 PM
        1991-03-31 14:10:00   R2  H  ...  43850.0   Sun 31-Mar-1991 2:10 PM
        ...                  ... ..  ...      ...                       ...
        2020-09-13 13:05:00  R17  A  ...   2735.0   Sun 13-Sep-2020 1:05 PM
        2020-09-19 16:40:00  R18  H  ...  17710.0   Sat 19-Sep-2020 4:40 PM
        [688 rows x 13 columns]

    >>> # The DataFrame can be sliced by Date in human-readable format!
    >>> ADE.games.loc['2016-01-01':'2019-12-31']
                             Rnd  T  ...    Crowd                     Date
        Date                         ...
        2016-03-26 19:25:00   R1  A  ...  25485.0  Sat 26-Mar-2016 7:25 PM
        2016-04-02 13:15:00   R2  H  ...  50555.0  Sat 02-Apr-2016 1:15 PM
        ...                  ... ..  ...      ...                      ...
        2019-08-17 16:05:00  R22  H  ...  48175.0  Sat 17-Aug-2019 4:05 PM
        2019-08-25 13:10:00  R23  A  ...   9560.0  Sun 25-Aug-2019 1:10 PM
        [93 rows x 13 columns]

    >>> # Let's see what columns are contained in the DataFrame
    >>> ADE.games.columns
        Index(['Rnd', 'T', 'Opponent', 'Scoring', 'For', 'Scoring', 'Against', 'Result', 'Margin', 'W-D-L', 'Venue', 'Crowd', 'Date'], dtype='object')

### Team.season_stats()

Retrieves the season stats for the specified year, including the individual player stats for all Players who played a game during the year. This function returns a Pandas DataFrame.

    >>> from pyAFL.teams import ADE

    >>> # Who player for Adelaide in 2019, and how did they perform? (See https://afltables.com/afl/stats/2019.html)
    >>> ADE.season_stats(2019)
                          #              Player               GM  ...     GA    %P  SU
        0                10        Boak, Travis               21  ...   14.0  79.8 NaN
        1                11       Rockliff, Tom               18  ...    8.0  77.3 NaN
        2                33  Byrne-Jones, Darcy               22  ...    7.0  84.0 NaN
        3                43        Houston, Dan               21  ...    3.0  82.1 NaN
        ...                                 ...                   ...              ...
        34               12     McKenzie, Trent                1  ...    NaN  94.0 NaN
        35               30          Atley, Joe                1  ...    NaN  68.0 NaN
        36               31      Johnson, Aidyn                1  ...    1.0  77.0 NaN
        [38 rows x 28 columns]

### Season()

Instantiates the Season object. This is a simple way to access match scores and results, leaving detailed team and player statistics to the `Team` and `Player` classes.
The **init** method finds the season on afltables.com based on the `year` argument integer.

### Season.get_season_stats()

Pulls season stats (ladders, matches, match summaries) and presents as a Python object.
This function returns a SeasonStats object with attributes:

- season_ladders (list): abbreviated ladders (dataframes) at end of each round
- season_matches (list): Match object for each match in the season
- match_summary (Pandas dataframe): summary of all matches in the season
- final_ladder (Pandas dataframe): the final season ladder (empty list if season is unfinished)

```
     >>> from pyAFL.seasons.models import Season
     
     # Instantiate Season object for 2021 (See https://afltables.com/afl/seas/2021.html)
     >>> season_2021 = Season(2021)
     >>> stats_2021 = season_2021.get_season_stats()
     >>> stats_2021.match_summary
     
     Date                Round  Game number   Venue    Home team  ...      Home team score detail         Away team score detail        Winning team     Margin     Year stage
     2021-03-18 18:25:00   1         1        M.C.G.   Richmond   ...     [3, 3, 8, 5, 10, 8, 15, 15]     [3, 2, 6, 6, 8, 12, 11, 14]     Richmond     25     Regular season
     2021-03-19 18:50:00   1         2        M.C.G.  Collingwood ...      [1, 2, 4, 6, 5, 7, 7, 11]       [3, 2, 6, 5, 9, 7, 10, 9]   Western Bulldogs     16     Regular season
     2021-03-20 12:45:00   1         3        M.C.G.   Melbourne ...       [4, 4, 7, 6, 9, 8, 11, 14]      [0, 4, 3, 8, 6, 9, 8, 10]    Melbourne     22     Regular season
     2021-03-20 15:35:00   1         4    Adelaide Oval Adelaide ...      [4, 4, 11, 7, 13, 9, 15, 13]     [2, 3, 5, 5, 10, 8, 13, 13]   Adelaide     12     Regular season
     2021-03-20 18:25:00   1         5      Docklands  Essendon  ...      [2, 4, 10, 6, 11, 10, 13, 13]    [3, 1, 4, 3, 12, 3, 14, 8]    Hawthorn     1     Regular season
    ...
```

## Testing

The unit tests can be run by running pytest from the project directory, like so;

    pytest

## Contributing

There is a lot to do so contributions are really appreciated! This is a great project for early stage developers to work with.

To begin it is recommended starting with issues labelled [good first issue](https://github.com/RamParameswaran/pyAFL/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).

How to get started:

1. Fork the pyAFL repo.
2. Create a new branch in you current repo from the 'master' branch with issue label.
3. 'Check out' the code with Git or [GitHub Desktop](https://desktop.github.com/)
4. Check [contributing.md](CONTRIBUTING.md)
5. Push commits and create a Pull Request (PR) to pyAFL
