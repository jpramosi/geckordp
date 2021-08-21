# pylint: disable=unused-import
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.inspector import InspectorActor
from geckordp.actors.walker import WalkerActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    current_tab = root.current_tab()
    tab = TabActor(cl, current_tab["actor"])
    tab
    actor_ids = tab.get_target()
    inspector = InspectorActor(cl, actor_ids["inspectorActor"])
    walker = WalkerActor(cl, inspector.get_walker()["actor"])
    return cl, walker


def test_document():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        assert val.get("actor", None) is not None
    finally:
        cl.disconnect()


def test_document_element():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        val = walker.document_element(val["actor"])
        assert val.get("actor", None) is not None
    finally:
        cl.disconnect()


def test_retain_node():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        val = walker.retain_node(val["actor"])
        assert response_valid("domwalker", val), str(val)
    finally:
        cl.disconnect()


def test_unretain_node():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        walker.retain_node(val["actor"])
        val = walker.unretain_node(val["actor"])
        assert response_valid("domwalker", val), str(val)
    finally:
        cl.disconnect()


def test_children():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        val = walker.children(val["actor"])
        assert isinstance(val, list)
        assert len(val) > 0
    finally:
        cl.disconnect()


def test_next_sibling():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        val = walker.children(val["actor"])[0]
        val = walker.next_sibling(val["actor"])
        assert val.get("actor", None) is not None
    finally:
        cl.disconnect()


def test_previous_sibling():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        val = walker.children(val["actor"])[0]
        val = walker.next_sibling(val["actor"])
        val = walker.previous_sibling(val["actor"])
        assert val.get("actor", None) is not None
    finally:
        cl.disconnect()


# # "Spec for 'domwalker' specifies a 'findInspectingNode' method that isn't implemented by the actor"
""" def test_find_inspecting_node():
    cl = None
    try:
        cl, walker = init()
        val = walker.find_inspecting_node()
    finally:
        cl.disconnect() """


def test_query_selector():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        val = walker.query_selector(val["actor"], "body h1")
        assert val.get("node", None) is not None
        assert val["node"].get("actor", None) is not None
    finally:
        cl.disconnect()


def test_query_selector_all():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        val = walker.query_selector_all(val["actor"], "body h1")
        assert val.get("actor", None) is not None
    finally:
        cl.disconnect()


def test_multi_frame_query_selector_all():
    cl = None
    try:
        cl, walker = init()
        val = walker.multi_frame_query_selector_all("body h1")
        assert val.get("actor", None) is not None
    finally:
        cl.disconnect()


def test_search():
    cl = None
    try:
        cl, walker = init()
        val = walker.search("body h1")
        assert val.get("list", None) is not None
    finally:
        cl.disconnect()


def test_get_suggestions_for_query():
    cl = None
    try:
        cl, walker = init()
        val = walker.get_suggestions_for_query("bod")
        assert val.get("list", None) is not None
    finally:
        cl.disconnect()


def test_add_pseudo_class_lock():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        val = walker.add_pseudo_class_lock(
            val["actor"], WalkerActor.PseudoClass.FOCUS, True)
        assert response_valid("domwalker", val), str(val)
    finally:
        cl.disconnect()


# "node.rawNode.classList is undefined"
""" def test_hide_node():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        val = walker.hide_node(val["actor"])
        log(val)
    finally:
        cl.disconnect() """


# "node.rawNode.classList is undefined"
""" def test_unhide_node():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        walker.hide_node(val["actor"])
        val = walker.unhide_node(val["actor"])
        log(val)
    finally:
        cl.disconnect() """


def test_remove_pseudo_class_lock():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        walker.add_pseudo_class_lock(
            val["actor"], WalkerActor.PseudoClass.FOCUS, True)
        val = walker.remove_pseudo_class_lock(
            val["actor"], WalkerActor.PseudoClass.FOCUS, True)
        assert response_valid("domwalker", val), str(val)
    finally:
        cl.disconnect()


# "InspectorUtils.clearPseudoClassLocks: Argument 1 does not implement interface Element."
""" def test_clear_pseudo_class_locks():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        walker.add_pseudo_class_lock(
            val["actor"], WalkerActor.PseudoClass.FOCUS, True)
        val = walker.clear_pseudo_class_locks(val["actor"])
        log(val)
    finally:
        cl.disconnect() """


def test_inner_html():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        val = walker.children(val["actor"])[0]
        val = walker.next_sibling(val["actor"])
        val = walker.inner_html(val["actor"])
        assert isinstance(val, str)
        assert "head" in val
    finally:
        cl.disconnect()


def test_set_inner_html():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        val = walker.children(val["actor"])[0]
        val = walker.next_sibling(val["actor"])
        html = walker.inner_html(val["actor"])
        val = walker.set_inner_html(val["actor"], html)
        assert response_valid("domwalker", val), str(val)
    finally:
        cl.disconnect()


def test_outer_html():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        val = walker.children(val["actor"])[0]
        val = walker.next_sibling(val["actor"])
        val = walker.outer_html(val["actor"])
        assert isinstance(val, str)
        assert "head" in val
    finally:
        cl.disconnect()


def test_set_outer_html():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        val = walker.children(val["actor"])[0]
        val = walker.next_sibling(val["actor"])
        html = walker.outer_html(val["actor"])
        val = walker.set_outer_html(val["actor"], html)
        assert response_valid("domwalker", val), str(val)
    finally:
        cl.disconnect()


def test_duplicate_node():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        val = walker.query_selector(val["actor"], "body h1")["node"]
        val = walker.duplicate_node(val["actor"])
        assert response_valid("domwalker", val), str(val)
    finally:
        cl.disconnect()


def test_remove_node():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        val = walker.query_selector(val["actor"], "body h1")["node"]
        val = walker.remove_node(val["actor"])
        assert val.get("nextSibling", None) is not None
    finally:
        cl.disconnect()


# this doesn't seem to work as expected:
# "Cannot remove document, document elements or dead nodes."
""" def test_remove_nodes():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        val = walker.query_selector(val["actor"], "body h1")["node"]
        walker.duplicate_node(val["actor"])
        val = walker.remove_nodes([val["actor"]])
        assert response_valid("domwalker", val), str(val)
    finally:
        cl.disconnect() """


def test_insert_before():
    cl = None
    try:
        cl, walker = init()
        # just check whether this function is available
        val = walker.insert_before("", "")
        assert response_valid("domwalker", val), str(val)
    finally:
        cl.disconnect()


def test_edit_tag_name():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        val = walker.query_selector(val["actor"], "body h1")["node"]
        val = walker.edit_tag_name(val["actor"], "h1")
        assert response_valid("domwalker", val), str(val)
    finally:
        cl.disconnect()


def test_get_mutations():
    cl = None
    try:
        cl, walker = init()
        val = walker.get_mutations(False)
        assert isinstance(val, list)
    finally:
        cl.disconnect()


def test_is_in_dom_tree():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        val = walker.query_selector(val["actor"], "body h1")["node"]
        val = walker.is_in_dom_tree(val["actor"])
        assert val.get("attached", None) is not None
    finally:
        cl.disconnect()


def test_get_node_actor_from_window_id():
    cl = None
    try:
        cl, walker = init()
        # just check whether this function is available
        val = walker.get_node_actor_from_window_id("")
        assert isinstance(val, dict)
    finally:
        cl.disconnect()


def test_get_node_actor_from_content_dom_reference():
    cl = None
    try:
        cl, walker = init()
        # just check whether this function is available
        val = walker.get_node_actor_from_content_dom_reference("")
        assert val.get("nodeFront", 0) != 0
    finally:
        cl.disconnect()


def test_get_style_sheet_owner_node():
    cl = None
    try:
        cl, walker = init()
        # just check whether this function is available
        val = walker.get_style_sheet_owner_node("")
        assert val.get("ownerNode", 0) != 0
    finally:
        cl.disconnect()


def test_get_node_from_actor():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        val = walker.query_selector(val["actor"], "body h1")["node"]
        val = walker.get_node_from_actor(val["actor"])
        assert val.get("node", None) is not None
    finally:
        cl.disconnect()


def test_get_layout_inspector():
    cl = None
    try:
        cl, walker = init()
        val = walker.get_layout_inspector()
        assert "layout" in val["actor"]
    finally:
        cl.disconnect()


def test_get_parent_grid_node():
    cl = None
    try:
        cl, walker = init()
        # just check whether this function is available
        val = walker.get_parent_grid_node("")
        assert val.get("node", 0) != 0
    finally:
        cl.disconnect()


def test_get_offset_parent():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        val = walker.query_selector(val["actor"], "body h1")["node"]
        val = walker.get_offset_parent(val["actor"])
        assert val.get("actor", None) is not None
    finally:
        cl.disconnect()


def test_set_mutation_breakpoints():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        val = walker.query_selector(val["actor"], "body h1")["node"]
        res = walker.set_mutation_breakpoints(
            val["actor"], False, False, False)
        assert "domwalker" in res["from"]
        res = walker.set_mutation_breakpoints(
            val["actor"], False, True, False)
        assert "domwalker" in res["from"]
    finally:
        cl.disconnect()


def test_get_embedder_element():
    cl = None
    try:
        cl, walker = init()
        # just check whether this function is available:
        # "browsingContext is null"
        val = walker.get_embedder_element("")
        assert "domwalker" in val["from"]
    finally:
        cl.disconnect()


def test_pick():
    cl = None
    try:
        cl, walker = init()
        val = walker.pick(False)
        assert response_valid("domwalker", val), str(val)
    finally:
        cl.disconnect()


def test_cancel_pick():
    cl = None
    try:
        cl, walker = init()
        val = walker.cancel_pick()
        assert response_valid("domwalker", val), str(val)
    finally:
        cl.disconnect()


def test_watch_root_node():
    cl = None
    try:
        cl, walker = init()
        val = walker.watch_root_node()
        assert response_valid("domwalker", val), str(val)
    finally:
        cl.disconnect()


def test_get_overflow_causing_elements():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        val = walker.query_selector(val["actor"], "body h1")["node"]
        val = walker.get_overflow_causing_elements(val["actor"])
        assert isinstance(val, dict)
    finally:
        cl.disconnect()


def test_get_scrollable_ancestor_node():
    cl = None
    try:
        cl, walker = init()
        val = walker.document()
        val = walker.query_selector(val["actor"], "body h1")["node"]
        val = walker.get_scrollable_ancestor_node(val["actor"])
        assert val.get("node", 0) != 0
    finally:
        cl.disconnect()


def test_release_node():
    cl = None
    try:
        cl, walker = init()
        # just check whether this function is available
        val = walker.release_node("")
        assert response_valid("domwalker", val), str(val)
    finally:
        cl.disconnect()


def test_release():
    cl = None
    try:
        cl, walker = init()
        val = walker.release()
        assert response_valid("domwalker", val), str(val)
    finally:
        cl.disconnect()
