# pylint: disable=unused-import
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.network_parent import NetworkParentActor
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
    watcher.watch_resources([
        WatcherActor.Resources.CONSOLE_MESSAGE,
        WatcherActor.Resources.ERROR_MESSAGE,
        WatcherActor.Resources.NETWORK_EVENT,
        WatcherActor.Resources.NETWORK_EVENT_STACKTRACE,
        WatcherActor.Resources.DOCUMENT_EVENT,
    ])
    network_parent = NetworkParentActor(
        cl, watcher.get_network_parent_actor()["network"]["actor"])
    return cl, network_parent


def test_set_network_throttling():
    cl = None
    try:
        cl, network_parent = init()
        val = network_parent.set_network_throttling(16, 16, 10)
        assert response_valid("networkParent", val), str(val)
    finally:
        cl.disconnect()


def test_get_network_throttling():
    cl = None
    try:
        cl, network_parent = init()
        val = network_parent.get_network_throttling()["state"]
        assert val is None
    finally:
        cl.disconnect()


def test_clear_network_throttling():
    cl = None
    try:
        cl, network_parent = init()
        val = network_parent.clear_network_throttling()
        assert response_valid("networkParent", val), str(val)
    finally:
        cl.disconnect()


def test_set_blocked_urls():
    cl = None
    try:
        cl, network_parent = init()
        val = network_parent.set_blocked_urls(
            ["example.com", ".js", "https://www.google.com/"])
        assert response_valid("networkParent", val), str(val)
    finally:
        cl.disconnect()


def test_get_blocked_urls():
    cl = None
    try:
        cl, network_parent = init()
        val = network_parent.get_blocked_urls()["urls"]
        assert len(val) == 0
    finally:
        cl.disconnect()
