# pylint: disable=unused-import
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.accessibility.parent_accessibility import ParentAccessibilityActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    root_ids = root.get_root()
    accessibility = ParentAccessibilityActor(
        cl, root_ids["parentAccessibilityActor"])
    accessibility.bootstrap()
    return cl, accessibility


def test_bootstrap():
    cl = None
    try:
        cl, accessibility = init()
        val = accessibility.bootstrap()
        assert val.get("state", None) is not None
    finally:
        cl.disconnect()


def test_enable():
    cl = None
    try:
        cl, accessibility = init()
        val = accessibility.enable()
        assert response_valid("parent", val), str(val)
    finally:
        cl.disconnect()


def test_disable():
    cl = None
    try:
        cl, accessibility = init()
        val = accessibility.disable()
        assert response_valid("parent", val), str(val)
    finally:
        cl.disconnect()
