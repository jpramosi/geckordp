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
from geckordp.actors.storage import IndexedDBStorageActor
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
            if ("indexedDB" in resource.get("actor", "")):
                fut.set_result(resource)

    cl.add_event_listener(
        watcher.actor_id, Events.Watcher.RESOURCE_AVAILABLE_FORM, on_resource)

    watcher.watch_targets(WatcherActor.Targets.FRAME)
    watcher.watch_resources([WatcherActor.Resources.INDEXED_DB])

    resource = fut.result(3.0)
    assert "actor" in resource

    storage_actor_id = resource.get("actor", "")
    indexed = IndexedDBStorageActor(cl, storage_actor_id)

    return cl, indexed


def test_get_store_objects():
    cl = None
    try:
        cl, indexed = init()
        val = indexed.get_store_objects("https://example.com")
        assert response_valid("indexedDB", val), str(val)
    finally:
        cl.disconnect()


def test_get_fields():
    cl = None
    try:
        cl, indexed = init()
        val = indexed.get_fields()
        assert response_valid("indexedDB", val), str(val)
    finally:
        cl.disconnect()


def test_remove_item():
    cl = None
    try:
        cl, indexed = init()
        val = indexed.remove_item("https://example.com", "x")
        assert response_valid("indexedDB", val), str(val)
    finally:
        cl.disconnect()
