# pylint: disable=unused-import
import pytest
import tests.helpers.utils as utils
import tests.helpers.constants as constants
from geckordp.rdp_client import RDPClient


def test_connect():
    cl = RDPClient()
    assert cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT) != None
    cl.disconnect()


def test_connect_context():
    with RDPClient(timeout_sec=3) as cl:
        cl.disconnect()
        assert cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT) != None


def test_connect_reconnect():
    with RDPClient(timeout_sec=3) as cl:
        assert cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT) != None
        cl.disconnect()
        assert cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT) != None
        cl.disconnect()


def test_connect_unspecified():
    with RDPClient(timeout_sec=3) as cl:
        assert cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT) != None


def test_connect_zero_timeout():
    with RDPClient(timeout_sec=0.0) as cl:
        assert cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT) == None


def test_connect_zero_timeout_unspecified():
    with RDPClient(timeout_sec=0.0) as cl:
        assert cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT) == None
        cl.disconnect()


# other tests will be covered with actors
