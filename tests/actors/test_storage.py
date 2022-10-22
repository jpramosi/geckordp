# pylint: disable=unused-import
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.storage import StorageActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    current_tab = root.current_tab()
    tab = TabActor(cl, current_tab["actor"])
    actor_ids = tab.get_target()
    storage = StorageActor(cl, actor_ids["storageActor"])
    return cl, storage


def test_list_stores():
    cl = None
    try:
        cl, storage = init()
        val = storage.list_stores()
        assert response_valid("storageActor", val), str(val)
    finally:
        cl.disconnect()
