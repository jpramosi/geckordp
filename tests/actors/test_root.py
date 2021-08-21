# pylint: disable=unused-import
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    return cl, root


def test_get_root():
    cl = None
    try:
        cl, root = init()
        val = root.get_root()["preferenceActor"]
        assert "server" in val and "conn" in val and "preferenceActor" in val
    finally:
        cl.disconnect()


def test_list_tabs():
    cl = None
    try:
        cl, root = init()
        val = root.list_tabs()
        assert len(val) == 1
        assert val[0]["url"] == "https://example.com/"
    finally:
        cl.disconnect()


def test_get_tab():
    cl = None
    try:
        cl, root = init()
        tab = root.list_tabs()[0]
        val = root.get_tab(tab["outerWindowID"])["tab"]
        assert val == tab
    finally:
        cl.disconnect()


def test_list_addons():
    cl = None
    try:
        cl, root = init()
        addons = root.list_addons()
        assert len(addons) >= 3
        val = addons[0]["actor"]
        assert "server" in val and "conn" in val and "webExtensionDescriptor" in val
    finally:
        cl.disconnect()


def test_list_workers():
    cl = None
    try:
        cl, root = init()
        workers = root.list_workers()
        assert len(workers) >= 2
        val = workers[0]["actor"]
        assert "server" in val and "conn" in val and "workerDescriptor" in val
    finally:
        cl.disconnect()


def test_list_service_worker_registrations():
    cl = None
    try:
        cl, root = init()
        workers = root.list_service_worker_registrations()
        assert len(workers) >= 0
    finally:
        cl.disconnect()


def test_list_processes():
    cl = None
    try:
        cl, root = init()
        processes = root.list_processes()
        assert len(processes) >= 2
        val = processes[0]["actor"]
        assert "server" in val and "conn" in val and "processDescriptor" in val
    finally:
        cl.disconnect()


def test_request_types():
    cl = None
    try:
        cl, root = init()
        types = root.request_types()
        assert len(types) >= 2
        assert "getRoot" in types and "listTabs" in types
    finally:
        cl.disconnect()


def test_echo():
    cl = None
    try:
        cl, root = init()
        types = root.echo("hello")
        assert types["text"] == "hello"
    finally:
        cl.disconnect()
