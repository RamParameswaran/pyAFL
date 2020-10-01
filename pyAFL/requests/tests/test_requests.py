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

    def test_noncached_request_runs_successfully_and_creates_cached_html(
        self, mock_python_get_request, mock_html_cache_dir
    ):
        test_path = os.path.join(
            requests.get_html_cache_path(), "players/TEST/FAKE_PLAYER.html"
        )

        # assert cached file does not exist yet
        assert not os.path.isfile(test_path)

        # make first request -> this will create the cached file
        resp = requests.get(
            "https://afltables.com/afl/stats/players/TEST/FAKE_PLAYER.html",
            force_live=True,
        )
        assert resp.status_code == 200
        assert "Hello test!" in resp.content.decode("utf-8")

        assert os.path.isfile(test_path)
        with open(test_path, "r") as f:
            html_on_file = f.read()
            assert "Hello test!" in html_on_file
        os.remove(test_path)

    def test_cached_request_fetches_from_cache_directory(
        self, mock_html_cache_dir, mock_python_get_request, monkeypatch
    ):
        test_path = os.path.join(
            requests.get_html_cache_path(), "players/TEST/TEST_PLAYER.html"
        )
        # assert cached file does not exist yet
        assert not os.path.isfile(test_path)

        # make first request -> this will create the cached file
        requests.get(
            "https://afltables.com/afl/stats/players/TEST/TEST_PLAYER.html",
            force_live=True,
        )

        # change the `python_requests.get` mock return_value
        resp2 = python_requests.models.Response()
        resp2.status_code = 404
        resp2._content = b"<html>Some error!</html>"
        monkeypatch.setattr(python_requests, "get", mock.Mock())
        python_requests.get.return_value = resp2

        # make second request
        resp = requests.get(
            "https://afltables.com/afl/stats/players/TEST/TEST_PLAYER.html"
        )

        # assert resp has not changed (because we fetched from cache)
        assert "Hello test!" in resp.content.decode("utf-8")