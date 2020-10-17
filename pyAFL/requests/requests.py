from bs4 import BeautifulSoup
import os
import re
import requests
from requests import Session as OriginalSession
import requests_cache
from requests_cache.core import CachedSession, _normalize_parameters
import sys
import urllib

from pyAFL import config


class AFLTablesCachedSession(CachedSession):
    def request(self, method, url, params=None, data=None, **kwargs):
        """
        This function overwrites the `CachedSession.request` method. The only difference
        is that in this function the HTML content is edited. Relative url hrefs are changed
        to absolute urls.

        The custom code is denoted by a the comment: "##### CUSTOMISED BLOCK #####".

        Returns
        ----------
        - Response object

        """
        response = super(CachedSession, self).request(
            method,
            url,
            _normalize_parameters(params),
            _normalize_parameters(data),
            **kwargs,
        )

        ##### CUSTOMISED BLOCK #####
        # Convert hrefs from relative to absolute urls from the https://www.afltables.com domain
        soup = BeautifulSoup(response.content, "html.parser")
        for link in soup.findAll("a"):
            if link.attrs.get("href") and "://" not in link.attrs.get("href"):
                link.attrs["href"] = urllib.parse.urljoin(url, link.attrs.get("href"))
        html_out = soup.prettify("utf-8")
        response._content = html_out
        ##### END CUSTOMISED BLOCK #####

        if self._is_cache_disabled:
            return response

        main_key = self.cache.create_key(response.request)

        # If self._return_old_data_on_error is set,
        # responses won't always have the from_cache attribute.
        if (
            hasattr(response, "from_cache")
            and not response.from_cache
            and self._filter_fn(response) is not True
        ):
            self.cache.delete(main_key)
            return response

        for r in response.history:
            self.cache.add_key_mapping(self.cache.create_key(r.request), main_key)
        return response


def get(url: str, force_live: bool = False):
    """
    This function is a wrapper around `requests.get`.
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

    if force_live:
        with requests_cache.disabled():
            # NOTE - when force_live == True - the anchor-tag absolute URL fix is not applied!
            return requests.get(url)
    else:
        return requests.get(url)


# Initalise cache backend
cache_name = "test_db" if "pytest" in sys.modules else "pyAFL_html_cache"
requests_cache.install_cache(
    cache_name, backend="sqlite", session_factory=AFLTablesCachedSession
)