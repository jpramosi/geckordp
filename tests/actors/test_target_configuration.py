# pylint: disable=unused-import
from logging import warning

import pytest

import tests.helpers.constants as constants
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.root import RootActor
from geckordp.actors.target_configuration import TargetConfigurationActor
from geckordp.actors.thread import ThreadActor
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
    target_cfg = TargetConfigurationActor(
        cl, watcher.get_target_configuration_actor()["actor"]
    )
    return cl, target_cfg


def test_update_configuration():
    cl = None
    try:
        cl, target_cfg = init()
        val = target_cfg.update_configuration(cache_disabled=True)
        assert response_valid("target-configuration", val), str(val)
    finally:
        cl.disconnect()
