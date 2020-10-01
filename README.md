![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)
![Python](https://img.shields.io/pypi/pyversions/django)
![Build and Test](https://github.com/RamParameswaran/pyAFL/workflows/Build%20and%20Test/badge.svg)

<p align="center">
     <img src="/static/img/AFL-logo.png" width="540" height="360">
</p>

# pyAFL

pyAFL is a AFL (Australian Football League) data fetching libary. It scrapes data from https://afltables.com/ and converts results to structured Python objects for easier analytics.

## Installation

1. Clone the repository locally:
   ```
   git clone https://github.com/RamParameswaran/pyAFL.git
   ```

## API

- Player data
  - [Player()](#Player)
  - [Player.get_player_stats()](#Player.get_player_stats)

### Player()

Instantiates the player by the provided 'name'. The name argument must be in the format "Firstname Lastname" and must be a name listed at https://afltables.com/afl/stats/playersA_idx.html

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
        [  St Kilda - 2001   ...8 columns],    St Kilda - 2002  ...8 columns],    St Kilda - 2003  ...8 columns],    St Kilda - 2004  ...8 columns],    St Kilda - 2005  ...8 columns],    St Kilda - 2006  ...8 columns],    St Kilda - 2007  ...8 columns],    St Kilda - 2008  ...8 columns],    St Kilda - 2009  ...8 columns],    St Kilda - 2010  ...8 columns],    St Kilda - 2011  ...8 columns],    St Kilda - 2012  ...8 columns],    St Kilda - 2013  ...8 columns],    St Kilda - 2014  ...8 columns], ...]

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
