# pylint: disable=unused-import
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.node_list import NodeListActor
from geckordp.actors.inspector import InspectorActor
from geckordp.actors.walker import WalkerActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    current_tab = root.current_tab()
    tab = TabActor(cl, current_tab["actor"])
    actor_ids = tab.get_target()
    inspector = InspectorActor(cl, actor_ids["inspectorActor"])
    walker = WalkerActor(cl, inspector.get_walker()["actor"])
    doc = walker.document()
    dom_node_list = walker.query_selector_all(doc["actor"], "body h1")
    node_list = NodeListActor(cl, dom_node_list["actor"])
    return cl, node_list


def test_item():
    cl = None
    try:
        cl, node_list = init()
        val = node_list.item(0)
        assert val.get("node", None) is not None
    finally:
        cl.disconnect()


def test_items():
    cl = None
    try:
        cl, node_list = init()
        val = node_list.items(0, 10000)
        assert val.get("nodes", None) is not None
    finally:
        cl.disconnect()


def test_release():
    cl = None
    try:
        cl, node_list = init()
        val = node_list.release()
        assert response_valid("domnodelist", val), str(val)
    finally:
        cl.disconnect()
