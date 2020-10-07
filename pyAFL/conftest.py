import os
import pytest
import requests_cache
from unittest import mock

from pyAFL.requests import requests


@pytest.fixture(autouse=True)
def create_test_db_before_test(request):
    filepath = os.path.join(os.getcwd(), "test_db.sqlite")
    if os.path.isfile(filepath):
        os.remove(filepath)
    requests_cache.install_cache(
        "test_db", backend="sqlite", session_factory=requests.AFLTablesCachedSession
    )
    yield
    if os.path.isfile(filepath):
        os.remove(filepath)