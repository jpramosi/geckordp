# pylint: disable=unused-import
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.descriptors.process import ProcessActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    processes = root.list_processes()
    process = ProcessActor(
        cl, processes[0]["actor"])
    return cl, process


def test_get_target():
    cl = None
    try:
        cl, process = init()
        val = process.get_target()["consoleActor"]
        assert "consoleActor" in val
    finally:
        cl.disconnect()


def test_get_watcher():
    cl = None
    try:
        cl, process = init()
        val = process.get_watcher()["actor"]
        assert "watcher" in val
    finally:
        cl.disconnect()
