import pytest
import requests
from requests_cache.models import CachedResponse, Response

from pyAFL.session import session


class TestRequestCaching:

    @pytest.fixture(autouse=True, scope="function")
    def before_each(self):
        session.cache.clear()

    def test_none_url_throws_exception(self):
        with pytest.raises(TypeError):
            session.get()

    def test_missing_url_schema_throws_exception(self):
        with pytest.raises(requests.exceptions.MissingSchema):
            session.get("abcdefgh")

    def test_invalid_url_throws_exception(self):
        with pytest.raises(requests.exceptions.ConnectionError):
            session.get("https://abcdefgh")

    def test_second_request_is_from_cache(self):
        url = "https://afltables.com/afl/stats/playersA_idx.html"

        resp1 = session.get(url)
        assert isinstance(resp1, Response)
        assert hasattr(resp1, "from_cache")
        assert not resp1.from_cache

        resp2 = session.get(url)
        assert isinstance(resp2, CachedResponse)
        assert hasattr(resp2, "from_cache")
        assert resp2.from_cache

    def test_all_requests_with_force_live_are_not_from_cache(self):
        url = "https://afltables.com/afl/stats/playersB_idx.html"

        resp1 = session.get(url, force_live=True)
        assert isinstance(resp1, Response)
        assert hasattr(resp1, "from_cache")
        assert not resp1.from_cache

        resp2 = session.get(url, force_live=True)
        assert isinstance(resp2, Response)
        assert hasattr(resp2, "from_cache")
        assert not resp2.from_cache

        resp3 = session.get(url, force_live=True)
        assert isinstance(resp3, Response)
        assert hasattr(resp3, "from_cache")
        assert not resp3.from_cache
