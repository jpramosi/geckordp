# pylint: disable=unused-import
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.accessibility.accessible import AccessibleActor
from geckordp.actors.accessibility.accessibility import AccessibilityActor
from geckordp.actors.accessibility.accessible_walker import AccessibleWalkerActor
from geckordp.actors.accessibility.parent_accessibility import ParentAccessibilityActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    current_tab = root.current_tab()
    tab = TabActor(cl, current_tab["actor"])
    actor_ids = tab.get_target()
    root_ids = root.get_root()
    accessibility = AccessibilityActor(cl, actor_ids["accessibilityActor"])
    accessibility.bootstrap()
    parent = ParentAccessibilityActor(
        cl, root_ids["parentAccessibilityActor"])
    parent.bootstrap()
    parent.enable()

    walker = AccessibleWalkerActor(cl,
                                   accessibility.get_walker()["actor"])
    children = walker.children()

    accessible = AccessibleActor(cl, children[0]["actor"])
    return cl, accessible


def test_audit():
    cl = None
    try:
        cl, accessible = init()
        val = accessible.audit()
        assert val.get("audit", None) is not None
    finally:
        cl.disconnect()


def test_children():
    cl = None
    try:
        cl, accessible = init()
        val = accessible.children()
        assert isinstance(val, list)
        assert len(val) > 0
    finally:
        cl.disconnect()


def test_get_relations():
    cl = None
    try:
        cl, accessible = init()
        val = accessible.get_relations()
        assert isinstance(val, list)
        assert len(val) > 0
    finally:
        cl.disconnect()


def test_hydrate():
    cl = None
    try:
        cl, accessible = init()
        val = accessible.hydrate()
        assert val.get("attributes", None) is not None
    finally:
        cl.disconnect()


def test_snapshot():
    cl = None
    try:
        cl, accessible = init()
        val = accessible.snapshot()
        log(val)
    finally:
        cl.disconnect()
