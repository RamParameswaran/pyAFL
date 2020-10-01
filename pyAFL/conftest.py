import pytest
from unittest import mock

from pyAFL.requests import requests


@pytest.fixture(scope="session")
def test_html_cache_path(tmpdir_factory):
    fn = tmpdir_factory.mktemp("__HTMLCACHE__")
    return fn


@pytest.fixture
def mock_html_cache_dir(monkeypatch, test_html_cache_path):
    monkeypatch.setattr(requests, "get_html_cache_path", mock.Mock())
    requests.get_html_cache_path.return_value = str(test_html_cache_path)