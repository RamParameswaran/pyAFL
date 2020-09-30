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

- Match details
  - [get_match_details()](#get_match_details)
- Player data
  - [get_player_details()](#get_player_details)

### get_match_details()

Pulls player career details for a specific match.

### get_player_details()

Pulls player career details for a specific player.

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
