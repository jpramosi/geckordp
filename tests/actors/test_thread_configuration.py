# pylint: disable=unused-import
from logging import warning

import pytest

import tests.helpers.constants as constants
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.root import RootActor
from geckordp.actors.thread import ThreadActor
from geckordp.actors.thread_configuration import ThreadConfigurationActor
from geckordp.actors.watcher import WatcherActor
from geckordp.logger import log, logdict
from geckordp.rdp_client import RDPClient
from tests.helpers.utils import *


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    current_tab = root.current_tab()
    tab = TabActor(cl, current_tab["actor"])
    watcher = WatcherActor(cl, tab.get_watcher()["actor"])
    thread_cfg = ThreadConfigurationActor(
        cl, watcher.get_thread_configuration_actor()["actor"]
    )
    return cl, thread_cfg


def test_update_configuration():
    cl = None
    try:
        cl, thread_cfg = init()
        val = thread_cfg.update_configuration(should_pause_on_debugger_statement=True)
        assert response_valid("thread-configuration", val), str(val)
    finally:
        cl.disconnect()
