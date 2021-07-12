# pylint: disable=unused-import
from time import sleep
import pytest
import tests.helpers.utils as utils
import tests.helpers.constants as constants
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.string import StringActor
from geckordp.actors.web_console import WebConsoleActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.targets.browsing_context import BrowsingContextActor
from geckordp.actors.events import Events
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    current_tab = root.current_tab()
    tab = TabActor(cl, current_tab["actor"])
    actor_ids = tab.get_target()
    BrowsingContextActor(cl, actor_ids["actor"]).attach()
    console = WebConsoleActor(cl, actor_ids["consoleActor"])
    return cl, console


def wrap_js(code: str):
    return "(() => { " + code + " })();"


def test_start_listeners():
    cl = None
    try:
        cl, console = init()
        listeners = []
        for listen in WebConsoleActor.Listeners:
            listeners.append(listen)
        val = console.start_listeners(listeners)["startedListeners"]
        for listen in WebConsoleActor.Listeners:
            assert listen in val
    finally:
        cl.disconnect()


def test_stop_listeners():
    cl = None
    try:
        cl, console = init()
        listeners = []
        for listen in WebConsoleActor.Listeners:
            listeners.append(listen)
        console.start_listeners(listeners)
        val = console.stop_listeners(listeners)["stoppedListeners"]
        for listen in WebConsoleActor.Listeners:
            assert listen in val
    finally:
        cl.disconnect()


def test_get_cached_messages():
    cl = None
    try:
        cl, console = init()
        val = console.get_cached_messages([
            WebConsoleActor.MessageTypes.PAGE_ERROR,
            WebConsoleActor.MessageTypes.CONSOLE_API])
        assert len(val["messages"]) >= 0
    finally:
        cl.disconnect()


def test_evaluate_js_async():
    cl = None
    try:
        cl, console = init()

        result_id = ""

        def on_eval(data):
            log(f"XXX:{data}")
            assert result_id == data["resultID"]
            assert data["result"] == "Example Domain"

        cl.add_event_listener(
            console.actor_id, Events.WebConsole.EVALUATION_RESULT, on_eval)

        response = console.evaluate_js_async(wrap_js("return document.title;"))
        result_id = response["resultID"]
        sleep(0.1)
    finally:
        cl.disconnect()


def test_evaluate_js_async_longstring():
    cl = None
    try:
        cl, console = init()

        size = 10000
        result_id = ""

        def on_eval(data):
            assert result_id == data["resultID"]
            assert data["result"]["type"] == "longString"
            string = StringActor(cl, data["result"]["actor"])
            val = string.substring(0, data["result"]["length"])
            assert len(val) == size

        cl.add_event_listener(
            console.actor_id, Events.WebConsole.EVALUATION_RESULT, on_eval)

        response = console.evaluate_js_async(wrap_js(f"""
            var size = {size}
            var buf = new Array(size);
            for(let i=0; i<size;i++)
                buf[i] = 'x';
            return buf.join('');
        """))
        result_id = response["resultID"]
        sleep(0.1)
    finally:
        cl.disconnect()


def test_autocomplete():
    cl = None
    try:
        cl, console = init()
        val = console.autocomplete("console.lo", 10)["matches"]
        assert "log" in val
    finally:
        cl.disconnect()


def test_clear_messages_cache():
    cl = None
    try:
        cl, console = init()
        console.clear_messages_cache()
    finally:
        cl.disconnect()


def test_block_request():
    cl = None
    try:
        cl, console = init()
        val = console.block_request("http://mm.com/")["from"]
        assert "consoleActor" in val
    finally:
        cl.disconnect()


def test_unblock_request():
    cl = None
    try:
        cl, console = init()
        val = console.unblock_request("http://mm.com/")["from"]
        assert "consoleActor" in val
    finally:
        cl.disconnect()
