# pylint: disable=unused-import
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.addon.web_extension_inspected_window import WebExtensionInspectedWindowActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    addons = root.list_addons()
    current_tab = root.current_tab()
    tab = TabActor(cl, current_tab["actor"])
    actor_ids = tab.get_target()
    webext = WebExtensionInspectedWindowActor(
        cl, actor_ids["webExtensionInspectedWindowActor"])
    addon = None
    for a in addons:
        if (a.get("url", None) is not None):
            addon = a
            break
    if (addon is None):
        print("WARNING: no addon available")
    return cl, addon, webext


def test_reload():
    cl = None
    try:
        cl, addon, webext = init()
        if (addon is None):
            return
        val = webext.reload(
            addon["url"], 1, addon["id"])
        assert response_valid(
            "webExtensionInspectedWindowActor", val), str(val)
    finally:
        cl.disconnect()


def test_eval():
    cl = None
    try:
        cl, addon, webext = init()
        if (addon is None):
            return
        val = webext.eval(
            "v = 10;", addon["url"], 1, addon["id"])
        assert "evalResult" in val
    finally:
        cl.disconnect()
