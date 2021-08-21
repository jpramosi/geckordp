# pylint: disable=unused-import
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.addon.addons import AddonsActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    root_ids = root.get_root()
    addons = AddonsActor(cl, root_ids["addonsActor"])
    return cl, addons


def test_install_temporary_addon():
    cl = None
    try:
        cl, _addons = init()
        # todo may not change anyway
        #val = addons.install_temporary_addon("")
    finally:
        cl.disconnect()
