from bs4 import BeautifulSoup
import os
import re
import requests as python_requests
import requests_cache
import sys
import urllib

from pyAFL import config


# Initalise cache backend
cache_name = "test_db" if "pytest" in sys.modules else "pyAFL_html_cache"
requests_cache.install_cache(cache_name, backend="sqlite")


def get(url: str, force_live: bool = False):
    """
    This function is a wrapper around `python_requests.get`.
    It saves the HTML response from previously-run get requests to file
    and fetches the cache from file for future requests.

    Parameters
    ----------
    url : str (required)
        url to get (including schema and domain)
    force_live : bool
        whether to force a live request request. This will overwrite the
        existing cached file (if one exists)

    Returns
    ----------
     - Response object (or exception from requests class)

    """

    # URL must be from https://afltables.com/afl/stats
    if not re.search(f"{config.AFLTABLES_STATS_BASE_URL}", url):
        raise AttributeError(
            f"This function only takes URLs from `{config.AFLTABLES_STATS_BASE_URL}`"
        )

    # get full filepath
    base_url = config.AFLTABLES_STATS_BASE_URL
    url_path = url.split(base_url)[-1]

    return python_requests.get(url)

    # otherwise make new live request and save html content to `__htmlcache__` directory
    resp = python_requests.get(url)
    if resp.status_code == 200:
        # 1) create subdirectories (if needed)
        path, basename = os.path.split(filepath)
        os.makedirs(path, exist_ok=True)

        # 2) convert hrefs from relative to absolute urls from the https://www.afltables.com domain
        soup = BeautifulSoup(resp.content, "html.parser")
        for link in soup.findAll("a"):
            link.attrs["href"] = urllib.parse.urljoin(url, link.attrs.get("href"))
        html_out = soup.prettify("utf-8")
        resp._content = html_out

        # 3) write file to cache file
        with open(filepath, "w+") as f:
            f.write(html_out.decode("utf-8"))

    return resp