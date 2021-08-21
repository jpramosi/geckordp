# pylint: disable=unused-import
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.device import DeviceActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    root_ids = root.get_root()
    device = DeviceActor(
        cl, root_ids["deviceActor"])
    return cl, device


def test_get_description():
    cl = None
    try:
        cl, device = init()
        val = device.get_description()["apptype"]
        assert val == "firefox"
    finally:
        cl.disconnect()
