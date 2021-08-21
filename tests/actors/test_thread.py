# pylint: disable=unused-import
from logging import warning
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.events import Events
from geckordp.actors.root import RootActor
from geckordp.actors.thread import ThreadActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.targets.browsing_context import BrowsingContextActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    current_tab = root.current_tab()
    tab = TabActor(cl, current_tab["actor"])
    actor_ids = tab.get_target()
    browser = BrowsingContextActor(
        cl, actor_ids["actor"])
    # todo add TargetConfigurationActor
    attach_ctx = browser.attach()
    thread = ThreadActor(
        cl, attach_ctx["threadActor"])
    val = thread.attach()
    assert response_valid("thread", val), str(val)
    return cl, thread


def test_reconfigure():
    cl = None
    try:
        cl, thread = init()
        val = thread.reconfigure()
        assert response_valid("thread", val), str(val)
    finally:
        cl.disconnect()


def test_interrupt_resume():
    cl = None
    try:
        cl, thread = init()
        val = thread.interrupt()["type"]
        assert val == "interrupt"
        val = thread.resume()
        assert response_valid("thread", val), str(val)
    finally:
        cl.disconnect()


def test_frames():
    cl = None
    try:
        cl, thread = init()
        thread.interrupt()
        val = thread.frames(0, 10)
        assert len(val) >= 0
    finally:
        cl.disconnect()


def test_sources():
    cl = None
    try:
        cl, thread = init()
        val = thread.sources()
        assert len(val) >= 0
    finally:
        cl.disconnect()


# see thread.py
""" 
def test_skip_breakpoints():
    cl = None
    try:
        cl, thread = init()
        val = thread.skip_breakpoints(True)
        logdict(val)
    finally:
        cl.disconnect()
"""


def test_dump_thread():
    cl = None
    try:
        cl, thread = init()
        val = thread.dump_thread().get("breakpoints", 0)
        assert val != 0
    finally:
        cl.disconnect()


# see thread.py
""" 
def test_dump_pools():
    cl = None
    try:
        cl, thread = init()
        val = thread.dump_pools()
        logdict(val)
    finally:
        cl.disconnect()
"""


def test_set_breakpoint():
    cl = None
    try:
        cl, thread = init()
        sources = thread.sources()
        if (len(sources) >= 0):
            print("WARNING: no sources available")
            return
        source = None
        for s in sources:
            if (s.get("actor", None) is not None):
                source = s
                break
        val = thread.set_breakpoint(
            0,
            0,
            source["sourceMapBaseURL"],
            source["actor"])
        assert response_valid("thread", val), str(val)
        val = thread.dump_thread()["breakpoints"][0]
        assert source["sourceMapBaseURL"] in val
    finally:
        cl.disconnect()


def test_remove_breakpoint():
    cl = None
    try:
        cl, thread = init()
        sources = thread.sources()
        if (len(sources) >= 0):
            print("WARNING: no sources available")
            return
        source = None
        for s in sources:
            if (s.get("actor", None) is not None):
                source = s
                break
        thread.set_breakpoint(
            0,
            0,
            source["sourceMapBaseURL"],
            source["actor"])
        val = thread.remove_breakpoint(
            0,
            0,
            source["sourceMapBaseURL"],
            source["actor"])
        assert response_valid("thread", val), str(val)
        val = thread.dump_thread()["breakpoints"]
        assert len(val) == 0
    finally:
        cl.disconnect()


def test_set_xhr_breakpoint():
    cl = None
    try:
        cl, thread = init()
        val = thread.set_xhr_breakpoint("xxxx.js", "GET")
        assert val == True
    finally:
        cl.disconnect()


def test_remove_xhr_breakpoint():
    cl = None
    try:
        cl, thread = init()
        val = thread.remove_xhr_breakpoint("xxxx.js", "GET")
        assert val == True
    finally:
        cl.disconnect()


def test_get_available_event_breakpoints():
    cl = None
    try:
        cl, thread = init()
        val = thread.get_available_event_breakpoints()
        assert len(val) > 0
    finally:
        cl.disconnect()


def test_get_active_event_breakpoints():
    cl = None
    try:
        cl, thread = init()
        val = thread.get_active_event_breakpoints()
        assert len(val) >= 0
    finally:
        cl.disconnect()


def test_set_active_event_breakpoints():
    cl = None
    try:
        cl, thread = init()
        val = thread.set_active_event_breakpoints(["xxxx"])
        assert response_valid("thread", val), str(val)
    finally:
        cl.disconnect()


def test_pause_on_exceptions():
    cl = None
    try:
        cl, thread = init()
        val = thread.pause_on_exceptions("", "")
        assert response_valid("thread", val), str(val)
    finally:
        cl.disconnect()


def test_toggle_event_logging():
    cl = None
    try:
        cl, thread = init()
        val = thread.toggle_event_logging("")
        assert response_valid("thread", val), str(val)
    finally:
        cl.disconnect()
        
""" 

def test_():
    cl = None
    try:
        cl, thread = init()
        val = thread.
        logdict(val)
    finally:
        cl.disconnect()

 """
