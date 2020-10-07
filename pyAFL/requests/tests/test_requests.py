import os
import pytest
import requests as python_requests
from unittest import mock

from pyAFL.requests import requests


class TestRequestCaching:
    @pytest.fixture
    def mock_python_get_request(self, monkeypatch):
        resp = python_requests.models.Response()
        resp.status_code = 200
        resp._content = b"<html>Hello test!</html>"

        monkeypatch.setattr(python_requests, "get", mock.Mock())
        python_requests.get.return_value = resp

    def test_none_url_throws_exception(self):
        with pytest.raises(TypeError):
            resp = requests.get()

    def test_missing_url_schema_throws_exception(self):
        with pytest.raises(AttributeError):
            resp = requests.get("abcdefgh")

    def test_invalid_url_throws_exception(self):
        with pytest.raises(AttributeError):
            resp = requests.get("https://abcdefgh")

    def test_second_request_is_from_cache(self):
        url = "https://afltables.com/afl/stats/playersA_idx.html"

        resp1 = requests.get(url)
        assert not resp1.from_cache

        resp2 = requests.get(url)
        assert resp2.from_cache
