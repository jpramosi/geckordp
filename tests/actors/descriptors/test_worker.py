# pylint: disable=unused-import
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.worker import WorkerActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    workers = root.list_workers()
    worker = WorkerActor(cl, workers[0]["actor"])
    return cl, worker


def test_detach():
    cl = None
    try:
        cl, worker = init()
        worker.detach()
    finally:
        cl.disconnect()


def test_get_target():
    cl = None
    try:
        cl, worker = init()
        val = worker.get_target()["type"]
        assert "connected" in val
    finally:
        cl.disconnect()
