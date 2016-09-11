import os
import pytest
import sys

from pytest_localserver.http import WSGIServer


@pytest.yield_fixture
def test_webserver(scope="session"):
    sys.path.append((os.path.normpath(os.path.join(__file__, "..", ".."))))
    import api

    server = WSGIServer(application=api.app)
    server.start()
    yield server
    server.stop()
