import pytest

from pytest_localserver.http import WSGIServer
from survey.router import app


@pytest.yield_fixture
def test_webserver(scope="session"):
    server = WSGIServer(application=app)
    server.start()
    yield server
    server.stop()
