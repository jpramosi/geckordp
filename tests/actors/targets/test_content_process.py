# pylint: disable=unused-import
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.process import ProcessActor
from geckordp.actors.targets.content_process import ContentProcessActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    processes = root.list_processes()
    content_process = None
    for p in processes:
        if (not p["isParent"]):
            process = ProcessActor(cl, p["actor"])
            content_process = ContentProcessActor(
                cl, process.get_target()["actor"])
            break
    return cl, content_process


def test_list_workers():
    cl = None
    try:
        cl, content_process = init()
        val = content_process.list_workers()
        assert len(val) >= 0
    finally:
        cl.disconnect()


def test_pause_matching_service_workers():
    cl = None
    try:
        cl, content_process = init()
        val = content_process.pause_matching_service_workers()
        assert response_valid("contentProcessTarget", val), str(val)
    finally:
        cl.disconnect()
