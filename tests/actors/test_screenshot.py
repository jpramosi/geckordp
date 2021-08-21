# pylint: disable=unused-import
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.screenshot import ScreenshotActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    current_tab = root.current_tab()
    tab = TabActor(cl, current_tab["actor"])
    actor_ids = tab.get_target()
    ctx_id = actor_ids["browsingContextID"]
    screenshot = ScreenshotActor(
        cl, root.get_root()["screenshotActor"])
    return cl, ctx_id, screenshot


def test_capture():
    cl = None
    try:
        cl, ctx_id, screenshot = init()
        val = screenshot.capture(ctx_id)["value"]["data"]
        assert len(val) > 1024
    finally:
        cl.disconnect()
