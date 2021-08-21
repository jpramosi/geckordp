# pylint: disable=unused-import
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.accessibility.accessibility import AccessibilityActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    current_tab = root.current_tab()
    tab = TabActor(cl, current_tab["actor"])
    actor_ids = tab.get_target()
    accessibility = AccessibilityActor(cl, actor_ids["accessibilityActor"])
    accessibility.bootstrap()
    return cl, accessibility


def test_get_traits():
    cl = None
    try:
        cl, accessibility = init()
        val = accessibility.get_traits()
        assert val.get("tabbingOrder", None) is not None
    finally:
        cl.disconnect()


def test_bootstrap():
    cl = None
    try:
        cl, accessibility = init()
        val = accessibility.bootstrap()
        assert len(val.keys()) > 0
    finally:
        cl.disconnect()


def test_get_walker():
    cl = None
    try:
        cl, accessibility = init()
        val = accessibility.get_walker()
        assert val.get("actor", None) is not None
    finally:
        cl.disconnect()


def test_get_simulator():
    cl = None
    try:
        cl, accessibility = init()
        val = accessibility.get_simulator()
        simulator_id = val.get("actor", None)
        if (simulator_id is None):
            log("No simulator actor found, firefox is probably running in headless mode")
    finally:
        cl.disconnect()
