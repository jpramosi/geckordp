# pylint: disable=unused-import
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.watcher import WatcherActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    current_tab = root.current_tab()
    tab = TabActor(cl, current_tab["actor"])
    tab.get_target()
    watcher = WatcherActor(cl, tab.get_watcher()["actor"])
    return cl, watcher


def test_watch_targets():
    cl = None
    try:
        cl, watcher = init()
        val = watcher.watch_targets(WatcherActor.Targets.FRAME)
        assert response_valid("watcher", val), str(val)
    finally:
        cl.disconnect()


def test_unwatch_targets():
    cl = None
    try:
        cl, watcher = init()
        watcher.unwatch_targets(WatcherActor.Targets.FRAME)
    finally:
        cl.disconnect()


def test_get_parent_browsing_context_id():
    cl = None
    try:
        cl, watcher = init()
        val = watcher.get_parent_browsing_context_id(0)
        assert response_valid("watcher", val), str(val)
    finally:
        cl.disconnect()


def test_watch_resources():
    cl = None
    try:
        cl, watcher = init()
        val = watcher.watch_resources([
            WatcherActor.Resources.NETWORK_EVENT,
            WatcherActor.Resources.NETWORK_EVENT_STACKTRACE,
            WatcherActor.Resources.DOCUMENT_EVENT,
        ])
        assert response_valid("watcher", val), str(val)
    finally:
        cl.disconnect()


def test_unwatch_resources():
    cl = None
    try:
        cl, watcher = init()
        watcher.unwatch_resources([
            WatcherActor.Resources.NETWORK_EVENT,
            WatcherActor.Resources.NETWORK_EVENT_STACKTRACE,
            WatcherActor.Resources.DOCUMENT_EVENT,
        ])
    finally:
        cl.disconnect()


def test_clear_resources():
    cl = None
    try:
        cl, watcher = init()
        watcher.clear_resources([
            WatcherActor.Resources.NETWORK_EVENT,
            WatcherActor.Resources.NETWORK_EVENT_STACKTRACE,
            WatcherActor.Resources.DOCUMENT_EVENT,
        ])
    finally:
        cl.disconnect()


def test_get_network_parent_actor():
    cl = None
    try:
        cl, watcher = init()
        val = watcher.get_network_parent_actor()
        assert response_valid("watcher", val), str(val)
    finally:
        cl.disconnect()


def test_get_blackboxing_actor():
    cl = None
    try:
        cl, watcher = init()
        val = watcher.get_blackboxing_actor()
        assert response_valid("watcher", val), str(val)
    finally:
        cl.disconnect()


def test_get_breakpoint_list_actor():
    cl = None
    try:
        cl, watcher = init()
        val = watcher.get_breakpoint_list_actor()
        assert response_valid("watcher", val), str(val)
    finally:
        cl.disconnect()


def test_get_target_configuration_actor():
    cl = None
    try:
        cl, watcher = init()
        val = watcher.get_target_configuration_actor()
        assert "configuration" in val["actor"]
    finally:
        cl.disconnect()


def test_get_thread_configuration_actor():
    cl = None
    try:
        cl, watcher = init()
        val = watcher.get_thread_configuration_actor()
        assert "configuration" in val["actor"]
    finally:
        cl.disconnect()
