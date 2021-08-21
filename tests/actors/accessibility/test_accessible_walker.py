# pylint: disable=unused-import
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
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
    walker = AccessibleWalkerActor(cl,
                                   accessibility.get_walker()["actor"])
    accessibility.bootstrap()
    parent = ParentAccessibilityActor(
        cl, root_ids["parentAccessibilityActor"])
    parent.bootstrap()
    parent.enable()
    return cl, walker


def test_children():
    cl = None
    try:
        cl, walker = init()
        val = walker.children()
        assert isinstance(val, list)
        assert len(val) > 0
    finally:
        cl.disconnect()


def test_get_accessible_for():
    cl = None
    try:
        cl, walker = init()
        # probably dom_node_actor from 'WalkerActor' expected, but empty string for testing is enough
        val = walker.get_accessible_for("")
        assert response_valid("accessible", val, True), str(val)
    finally:
        cl.disconnect()


def test_get_ancestry():
    cl = None
    try:
        cl, walker = init()
        val = walker.get_ancestry("")
        assert isinstance(val, list)
    finally:
        cl.disconnect()


def test_start_audit():
    cl = None
    try:
        cl, walker = init()
        val = walker.start_audit()
        assert response_valid("accessible", val), str(val)
    finally:
        cl.disconnect()


def test_highlight_accessible():
    cl = None
    try:
        cl, walker = init()
        val = walker.highlight_accessible("")
        assert val.get("value", None) is not None
    finally:
        cl.disconnect()


def test_unhighlight():
    cl = None
    try:
        cl, walker = init()
        val = walker.unhighlight()
        assert response_valid("accessible", val), str(val)
    finally:
        cl.disconnect()


def test_cancel_pick():
    cl = None
    try:
        cl, walker = init()
        val = walker.cancel_pick()
        assert response_valid("accessible", val), str(val)
    finally:
        cl.disconnect()


def test_pick_and_focus():
    cl = None
    try:
        cl, walker = init()
        val = walker.pick_and_focus()
        assert response_valid("accessible", val), str(val)
    finally:
        cl.disconnect()


def test_show_tabbing_order():
    cl = None
    try:
        cl, walker = init()
        val = walker.show_tabbing_order("", 0)
        assert response_valid("accessible", val), str(val)
    finally:
        cl.disconnect()
