# pylint: disable=unused-import
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.memory import MemoryActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    current_tab = root.current_tab()
    tab = TabActor(cl, current_tab["actor"])
    actor_ids = tab.get_target()
    memory = MemoryActor(cl, actor_ids["memoryActor"])
    return cl, memory


def test_attach():
    cl = None
    try:
        cl, memory = init()
        val = memory.attach()
        assert val["type"] == "attached"
    finally:
        cl.disconnect()


def test_detach():
    cl = None
    try:
        cl, memory = init()
        memory.attach()
        val = memory.detach()
        assert val["type"] == "detached"
    finally:
        cl.disconnect()


def test_get_state():
    cl = None
    try:
        cl, memory = init()
        val = memory.get_state()
        assert val["state"] == "detached"
    finally:
        cl.disconnect()


def test_take_census():
    cl = None
    try:
        cl, memory = init()
        memory.attach()
        val = memory.take_census()
        assert len(val["objects"]) > 5
        assert isinstance(val["domNode"], dict)
    finally:
        cl.disconnect()


def test_start_recording_allocations():
    cl = None
    try:
        cl, memory = init()
        memory.attach()
        val = memory.start_recording_allocations()
        assert isinstance(val["value"], float)
    finally:
        cl.disconnect()


def test_stop_recording_allocations():
    cl = None
    try:
        cl, memory = init()
        memory.attach()
        memory.start_recording_allocations()
        val = memory.stop_recording_allocations()
        assert isinstance(val["value"], float)
    finally:
        cl.disconnect()


def test_get_allocations_settings():
    cl = None
    try:
        cl, memory = init()
        memory.attach()
        val = memory.get_allocations_settings()
        assert isinstance(val["options"], dict)
    finally:
        cl.disconnect()


def test_get_allocations():
    cl = None
    try:
        cl, memory = init()
        memory.attach()
        memory.start_recording_allocations()
        val = memory.get_allocations()
        assert val.get("allocations", None) is not None
    finally:
        cl.disconnect()


def test_force_garbage_collection():
    cl = None
    try:
        cl, memory = init()
        memory.attach()
        val = memory.force_garbage_collection()
        assert response_valid("memory", val), str(val)
    finally:
        cl.disconnect()


def test_force_cycle_collection():
    cl = None
    try:
        cl, memory = init()
        memory.attach()
        val = memory.force_cycle_collection()
        assert response_valid("memory", val), str(val)
    finally:
        cl.disconnect()


def test_measure():
    cl = None
    try:
        cl, memory = init()
        memory.attach()
        val = memory.measure()
        assert val.get("total", None) is not None
    finally:
        cl.disconnect()


def test_resident_unique():
    cl = None
    try:
        cl, memory = init()
        memory.attach()
        val = memory.resident_unique()
        assert isinstance(val["value"], int)
    finally:
        cl.disconnect()


def test_save_heap_snapshot():
    cl = None
    try:
        cl, memory = init()
        memory.attach()
        val = memory.save_heap_snapshot()
        assert isinstance(val, str) and len(val) > 0
    finally:
        cl.disconnect()
