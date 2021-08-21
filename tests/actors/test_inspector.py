# pylint: disable=unused-import
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.inspector import InspectorActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    current_tab = root.current_tab()
    tab = TabActor(cl, current_tab["actor"])
    actor_ids = tab.get_target()
    inspector = InspectorActor(cl, actor_ids["inspectorActor"])
    return cl, inspector


def test_get_walker():
    cl = None
    try:
        cl, inspector = init()
        val = inspector.get_walker()["actor"]
        assert "domwalker" in val
    finally:
        cl.disconnect()


def test_get_page_style():
    cl = None
    try:
        cl, inspector = init()
        val = inspector.get_page_style()["pageStyle"]["actor"]
        assert "pagestyle" in val
    finally:
        cl.disconnect()


def test_get_compatibility():
    cl = None
    try:
        cl, inspector = init()
        val = inspector.get_compatibility()["compatibility"]["actor"]
        assert "compatibility" in val
    finally:
        cl.disconnect()


def test_get_highlighter_by_type():
    cl = None
    try:
        cl, inspector = init()
        val = inspector.get_highlighter_by_type(InspectorActor.Highlighters.SELECTOR_HIGHLIGHTER)["highlighter"]["actor"]
        assert "customhighlighter" in val
    finally:
        cl.disconnect()


def test_get_image_data_from_url():
    cl = None
    try:
        cl, inspector = init()
        val = inspector.get_image_data_from_url(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Example.jpg/116px-Example.jpg")["data"]["length"]
        assert int(val) >= 0
    finally:
        cl.disconnect()


def test_resolve_relative_url():
    cl = None
    try:
        cl, inspector = init()
        val = inspector.resolve_relative_url("https://duckduckgo.com/", "")["value"]
        assert val == "https://duckduckgo.com/"
    finally:
        cl.disconnect()


def test_pick_color_from_page():
    cl = None
    try:
        cl, inspector = init()
        val = inspector.pick_color_from_page(
            {"copyOnSelect": True, "fromMenu": True})
        assert response_valid("inspectorActor", val), str(val)
    finally:
        cl.disconnect()


def test_cancel_pick_color_from_page():
    cl = None
    try:
        cl, inspector = init()
        val = inspector.cancel_pick_color_from_page()
        assert response_valid("inspectorActor", val), str(val)
    finally:
        cl.disconnect()


def test_supports_highlighters():
    cl = None
    try:
        cl, inspector = init()
        val = inspector.supports_highlighters()["value"]
        assert val == True
    finally:
        cl.disconnect()
