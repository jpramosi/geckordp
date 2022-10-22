# pylint: disable=unused-import
from concurrent.futures import Future
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.events import Events
from geckordp.actors.watcher import WatcherActor
from geckordp.actors.storage import LocalStorageActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    current_tab = root.current_tab()
    tab = TabActor(cl, current_tab["actor"])
    watcher_ctx = tab.get_watcher()
    watcher = WatcherActor(
        cl, watcher_ctx["actor"])

    resource = {}
    fut = Future()

    async def on_resource(data: dict):
        resources = data.get("resources", [])
        for resource in resources:
            if ("local" in resource.get("actor", "")):
                fut.set_result(resource)

    actor_ids = tab.get_target()
    window_global_actor = actor_ids["actor"]
    cl.add_event_listener(
        window_global_actor, Events.Watcher.RESOURCE_AVAILABLE_FORM, on_resource)

    watcher.watch_targets(WatcherActor.Targets.FRAME)
    watcher.watch_resources([WatcherActor.Resources.LOCAL_STORAGE])

    resource = fut.result(3.0)
    assert "actor" in resource

    storage_actor_id = resource.get("actor", "")
    local = LocalStorageActor(cl, storage_actor_id)

    return cl, local


def test_get_store_objects():
    cl = None
    try:
        cl, local = init()
        val = local.get_store_objects("https://example.com")
        assert response_valid("localStorage", val), str(val)
    finally:
        cl.disconnect()


def test_get_fields():
    cl = None
    try:
        cl, local = init()
        val = local.get_fields()
        assert response_valid("localStorage", val), str(val)
    finally:
        cl.disconnect()


def test_add_item():
    cl = None
    try:
        cl, local = init()
        val = local.add_item("x", "https://example.com")
        assert response_valid("localStorage", val), str(val)
    finally:
        cl.disconnect()


def test_remove_item():
    cl = None
    try:
        cl, local = init()
        val = local.remove_item("https://example.com", "x")
        assert response_valid("localStorage", val), str(val)
    finally:
        cl.disconnect()


def test_edit_item():
    cl = None
    try:
        cl, local = init()
        val = local.edit_item({})
        assert response_valid("localStorage", val), str(val)
    finally:
        cl.disconnect()


def test_remove_all():
    cl = None
    try:
        cl, local = init()
        val = local.remove_all("https://example.com")
        assert response_valid("localStorage", val), str(val)
    finally:
        cl.disconnect()
