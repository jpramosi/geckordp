# pylint: disable=unused-import
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.descriptors.web_extension import WebExtensionActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    addons = root.list_addons()
    current_tab = root.current_tab()
    tab = TabActor(cl, current_tab["actor"])
    actor_ids = tab.get_target()
    webext = None
    addon = None
    for a in addons:
        if (a.get("url", None) is not None):
            addon = a
            webext = WebExtensionActor(
                cl, addon["actor"])
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
        val = webext.reload()
        assert response_valid(
            "webExtensionDescriptor", val), str(val)
    finally:
        cl.disconnect()


def test_connect():
    cl = None
    try:
        cl, addon, webext = init()
        if (addon is None):
            return
        val = webext.connect()
        assert response_valid(
            "webExtensionDescriptor", val), str(val)
    finally:
        cl.disconnect()


def test_get_target():
    cl = None
    try:
        cl, addon, webext = init()
        if (addon is None):
            return
        val = webext.get_target()
        assert response_valid(
            "webExtensionDescriptor", val), str(val)
    finally:
        cl.disconnect()
