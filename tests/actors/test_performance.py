# pylint: disable=unused-import
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.performance import PerformanceActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    current_tab = root.current_tab()
    tab = TabActor(cl, current_tab["actor"])
    actor_ids = tab.get_target()
    performance = PerformanceActor(cl, actor_ids["performanceActor"])
    performance.connect()
    return cl, performance


def test_connect():
    cl = None
    try:
        cl, performance = init()
        val = performance.connect()
        assert val.get("traits", None) is not None
    finally:
        cl.disconnect()


def test_can_currently_record():
    cl = None
    try:
        cl, performance = init()
        val = performance.can_currently_record()
        assert val.get("value", None) is not None
    finally:
        cl.disconnect()


def test_start_recording():
    cl = None
    try:
        cl, performance = init()
        val = performance.start_recording()
        assert val.get("actor", None) is not None
    finally:
        cl.disconnect()


def test_stop_recording():
    cl = None
    try:
        cl, performance = init()
        val = performance.start_recording()
        val = performance.stop_recording(val.get("actor", ""))
        assert val.get("actor", None) is not None
    finally:
        cl.disconnect()


def test_is_recording():
    cl = None
    try:
        cl, performance = init()
        val = performance.is_recording()
        assert isinstance(val, bool)
    finally:
        cl.disconnect()


def test_get_recordings():
    cl = None
    try:
        cl, performance = init()
        val = performance.get_recordings()
        assert isinstance(val, list)
    finally:
        cl.disconnect()


def test_get_configuration():
    cl = None
    try:
        cl, performance = init()
        val = performance.get_configuration()
        assert isinstance(val, dict)
        assert val.get("interval", None) is not None
    finally:
        cl.disconnect()


def test_set_profiler_status_interval():
    cl = None
    try:
        cl, performance = init()
        performance.set_profiler_status_interval(100)
    finally:
        cl.disconnect()
