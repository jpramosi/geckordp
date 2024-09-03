# pylint: disable=unused-import
from time import sleep

import pytest

import tests.helpers.constants as constants
from geckordp.actors.descriptors.process import ProcessActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.events import Events
from geckordp.actors.network_event import NetworkEventActor
from geckordp.actors.resources import Resources
from geckordp.actors.root import RootActor
from geckordp.actors.targets.window_global import WindowGlobalActor
from geckordp.actors.thread import ThreadActor
from geckordp.actors.watcher import WatcherActor
from geckordp.actors.web_console import WebConsoleActor
from geckordp.logger import log, logdict
from geckordp.rdp_client import RDPClient
from tests.helpers.utils import *


def test_network_event():
    cl = None
    try:
        cl = RDPClient(3)
        cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
        root = RootActor(cl)
        process_descriptors = root.list_processes()

        for descriptor in process_descriptors:
            actor_id = descriptor["actor"]
            process_actor_ids = ProcessActor(cl, actor_id).get_target()

            console = WebConsoleActor(cl, process_actor_ids["consoleActor"])
            console.start_listeners([])

        current_tab = root.current_tab()
        tab = TabActor(cl, current_tab["actor"])
        actor_ids = tab.get_target()

        browser = WindowGlobalActor(cl, actor_ids["actor"])

        console = WebConsoleActor(cl, actor_ids["consoleActor"])
        console.start_listeners([])

        watcher_ctx = tab.get_watcher()
        watcher = WatcherActor(cl, watcher_ctx["actor"])

        thread = ThreadActor(cl, actor_ids["threadActor"])
        thread.attach()

        # todo add TargetConfigurationActor

        watcher.watch_resources(
            [
                Resources.CONSOLE_MESSAGE,
                Resources.ERROR_MESSAGE,
                Resources.NETWORK_EVENT,
                Resources.NETWORK_EVENT_STACKTRACE,
                Resources.DOCUMENT_EVENT,
            ]
        )

        network_event_ids = []

        def on_resource_available(data):
            array = data.get("array", [])
            for sub_array in array:
                sub_array: list
                for i, item in enumerate(sub_array):
                    item: str | list
                    if isinstance(item, str) and "network-event" in item:
                        # obj[i + 1] = next item in array
                        for obj in sub_array[i + 1]:
                            obj: dict
                            actor_id = obj.get("actor", "")
                            resource_id = obj.get("resourceId", -1)
                            if "netEvent" in actor_id and resource_id != -1:
                                network_event_ids.append(actor_id)

        cl.add_event_listener(
            watcher_ctx["actor"],
            Events.Watcher.RESOURCES_AVAILABLE_ARRAY,
            on_resource_available,
        )

        browser.navigate_to("https://example.com/")
        sleep(1.5)
        network_event = NetworkEventActor(cl, network_event_ids[0])

        # get_request_headers
        val = network_event.get_request_headers()["headers"]
        assert len(val) > 2

        # get_request_cookies
        val = network_event.get_request_cookies().get("cookies", 0)
        assert val != 0

        # get_request_post_data
        val = network_event.get_request_post_data().get("postData", 0)
        assert val != 0

        # get_response_headers
        val = network_event.get_response_headers()["headers"]
        assert isinstance(val, list)

        # get_response_cookies
        val = network_event.get_response_cookies().get("cookies", 0)
        assert val != 0

        # get_response_cache
        val = network_event.get_response_cache()
        assert response_valid("netEvent", val), str(val)

        # get_response_content
        val = network_event.get_response_content()["content"]["size"]
        assert val > 100

        # get_event_timings
        val = network_event.get_event_timings().get("timings", 0)
        assert val != 0

        # get_security_info
        val = network_event.get_security_info()["securityInfo"]["state"]
        assert val == "secure"

    finally:
        cl.disconnect()
