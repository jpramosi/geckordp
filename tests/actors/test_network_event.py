# pylint: disable=unused-import
from time import sleep
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.network_content import NetworkContentActor
from geckordp.actors.network_event import NetworkEventActor
from geckordp.actors.web_console import WebConsoleActor
from geckordp.actors.targets.browsing_context import BrowsingContextActor
from geckordp.actors.watcher import WatcherActor
from geckordp.actors.event_source import EventSourceActor
from geckordp.actors.web_socket import WebSocketActor
from geckordp.actors.descriptors.process import ProcessActor
from geckordp.actors.targets.content_process import ContentProcessActor
from geckordp.actors.thread import ThreadActor
from geckordp.actors.events import Events
from geckordp.logger import log, logdict


def test_network_event():
    cl = None
    try:
        cl = RDPClient(3)
        cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
        root = RootActor(cl)
        process_descriptors = root.list_processes()

        for descriptor in process_descriptors:
            actor_id = descriptor["actor"]
            process_actor_ids = ProcessActor(
                cl, actor_id).get_target()

            console = WebConsoleActor(
                cl, process_actor_ids["consoleActor"])
            console.start_listeners([])

        current_tab = root.current_tab()
        tab = TabActor(cl, current_tab["actor"])
        actor_ids = tab.get_target()

        browser = BrowsingContextActor(
            cl, actor_ids["actor"])
        browser_context = browser.attach()

        console = WebConsoleActor(
            cl, actor_ids["consoleActor"])
        console.start_listeners([])

        watcher_ctx = tab.get_watcher()
        watcher = WatcherActor(
            cl, watcher_ctx["actor"])

        thread = ThreadActor(
            cl, browser_context["threadActor"])
        thread.attach()

        # todo add TargetConfigurationActor

        watcher.watch_resources([
            WatcherActor.Resources.CONSOLE_MESSAGE,
            WatcherActor.Resources.ERROR_MESSAGE,
            WatcherActor.Resources.NETWORK_EVENT,
            WatcherActor.Resources.NETWORK_EVENT_STACKTRACE,
            WatcherActor.Resources.DOCUMENT_EVENT,
        ])

        network_event_ids = []

        def on_resource_available(data):
            resources = data["resources"]
            if (len(resources) <= 0):
                return
            resources = resources[0]
            if (resources["resourceType"] != "network-event"):
                return
            network_event_actor_id = resources["actor"]
            resource_id = resources.get("resourceId", -1)
            if (resource_id == -1):
                return
            network_event_ids.append(network_event_actor_id)

        cl.add_event_listener(
            watcher_ctx["actor"],
            Events.Watcher.RESOURCE_AVAILABLE_FORM,
            on_resource_available)

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
