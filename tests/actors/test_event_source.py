# pylint: disable=unused-import
import pytest
import tests.helpers.constants as constants
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.event_source import EventSourceActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    current_tab = root.current_tab()
    tab = TabActor(cl, current_tab["actor"])
    actor_ids = tab.get_target()
    event_source = EventSourceActor(cl, actor_ids["eventSourceActor"])
    return cl, event_source


def test_start_listening():
    cl = None
    try:
        cl, event_source = init()
        event_source.start_listening()
    finally:
        cl.disconnect()


def test_stop_listening():
    cl = None
    try:
        cl, event_source = init()
        event_source.stop_listening()
    finally:
        cl.disconnect()
