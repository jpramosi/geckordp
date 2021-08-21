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
        if ("fill" in a.get("name", "")):
            addon = a
            break
    return cl, addon, webext


def test_reload():
    cl = None
    try:
        cl, addon, webext = init()
        val = webext.reload(
            "", 1, addon["id"])
        assert response_valid("webExtension", val), str(val)
    finally:
        cl.disconnect()


def test_eval():
    cl = None
    try:
        cl, addon, webext = init()
        val = webext.eval(
            "v = 10;", "", 1, addon["id"])["evalResult"]["value"]
        assert val == 10
    finally:
        cl.disconnect()
