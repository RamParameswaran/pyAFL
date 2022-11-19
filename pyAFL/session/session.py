import sys
import urllib
from datetime import timedelta

from bs4 import BeautifulSoup
from requests_cache import CachedSession
from requests_cache.models import AnyResponse


class __AFLTablesCachedSession(CachedSession):

    def request(
        self,
        method: str,
        url: str,
        *args,
        **kwargs,
    ) -> AnyResponse:
        response = super().request(method, url, **kwargs)
        self.cache.save_response(self.post_process(url, response))
        return response

    def post_process(self, url: str, response: AnyResponse):
        """ Converts the relative urls to absolute urls.
            - Parses the response html
            - Finds all <a> tags
            - If the `href` value is a relative url, prepend it with the current request url.

            Reasoning:
            - afltable.com uses relative urls (eg `../teams/richmond_idx.html` rather
            than `https://afltables.com/afl/teams/richmond_idx.html`).
        """
        soup = BeautifulSoup(response.content, "html.parser")
        for link in soup.findAll("a"):
            if link.attrs.get("href") and "://" not in link.attrs.get("href"):
                link.attrs["href"] = urllib.parse.urljoin(url, link.attrs.get("href"))
        html_out = soup.prettify("utf-8")
        response._content = html_out

        return response

    def get(self, url, force_live=False, **kwargs) -> AnyResponse:
        # If `force_live` kwarg is provided, disable request cache.
        if force_live:
            with self.cache_disabled():
                return super().get(url, **kwargs)

        # Else apply normal request caching logic
        return super().get(url, **kwargs)


session = __AFLTablesCachedSession(
    "test_db" if "pytest" in sys.modules else "pyAFL_html_cache",
    backend="filesystem",
    use_cache_dir=True,                # Save files in the default user cache dir
    cache_control=False,               # Use Cache-Control response headers for expiration, if available
    expire_after=timedelta(days=365),  # Otherwise expire responses after one day
    allowable_codes=[200],             # Cache 400 responses as a solemn reminder of your failures
    allowable_methods=['GET'],         # Cache whatever HTTP methods you want
    stale_if_error=False,               # In case of request errors, use stale cache data if possible
)
