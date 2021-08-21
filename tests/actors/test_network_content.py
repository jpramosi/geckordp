# pylint: disable=unused-import
import pytest
import tests.helpers.utils as utils
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.network_content import NetworkContentActor
from geckordp.actors.watcher import WatcherActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    current_tab = root.current_tab()
    tab = TabActor(cl, current_tab["actor"])
    actor_ids = tab.get_target()
    network_content = NetworkContentActor(cl, actor_ids["networkContentActor"])
    watcher = WatcherActor(cl, tab.get_watcher()["actor"])
    return cl, network_content, watcher


def test_send_http_request_get_stack_trace():
    cl = None
    try:
        cl, network_content, watcher = init()
        watcher.watch_resources(
            [WatcherActor.Resources.NETWORK_EVENT_STACKTRACE])
        val = network_content.send_http_request(
            method="GET",
            url="https://example.com/",
            headers={
                "Host": "example.com",
                "User-Agent": "special-agent-007"
            },
            body="my name is bond, james bond")["channelId"]
        assert val > 0
        val = network_content.get_stack_trace(val).get("stacktrace", 0)
        assert val != 0
    finally:
        cl.disconnect()
