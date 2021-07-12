""" This example demonstrates the initialization procedure of every available actor.
"""
# pylint: disable=unused-variable
# pylint: disable=invalid-name
import argparse
import json
from geckordp.rdp_client import RDPClient
from geckordp.actors.events import Events
from geckordp.actors.root import RootActor
from geckordp.actors.addon.addons import AddonsActor
from geckordp.actors.addon.web_extension_inspected_window import WebExtensionInspectedWindowActor
from geckordp.actors.descriptors.process import ProcessActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.descriptors.web_extension import WebExtensionActor
from geckordp.actors.descriptors.worker import WorkerActor
from geckordp.actors.targets.browsing_context import BrowsingContextActor
from geckordp.actors.targets.content_process import ContentProcessActor
from geckordp.actors.device import DeviceActor
from geckordp.actors.event_source import EventSourceActor
from geckordp.actors.inspector import InspectorActor
from geckordp.actors.network_content import NetworkContentActor
from geckordp.actors.network_event import NetworkEventActor
from geckordp.actors.network_parent import NetworkParentActor
from geckordp.actors.performance import PerformanceActor
from geckordp.actors.preference import PreferenceActor
from geckordp.actors.screenshot import ScreenshotActor
from geckordp.actors.source import SourceActor
from geckordp.actors.string import StringActor
from geckordp.actors.target_configuration import TargetConfigurationActor
from geckordp.actors.thread import ThreadActor
from geckordp.actors.walker import WalkerActor
from geckordp.actors.watcher import WatcherActor
from geckordp.actors.web_console import WebConsoleActor
from geckordp.actors.web_socket import WebSocketActor
from geckordp.profile import ProfileManager
from geckordp.firefox import Firefox


""" Uncomment to enable debug output
"""
#from geckordp.settings import GECKORDP
#GECKORDP.DEBUG = 1
#GECKORDP.DEBUG_REQUEST = 1
#GECKORDP.DEBUG_RESPONSE = 1


def main():
    # parse arguments
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--host', type=str, default="localhost",
                        help="The host to connect to")
    parser.add_argument('--port', type=int, default="6000",
                        help="The port to connect to")
    args, _ = parser.parse_known_args()

    # clone default profile to 'geckordp'
    pm = ProfileManager()
    profile_name = "geckordp"
    pm.clone("default-release", profile_name)
    profile = pm.get_profile_by_name(profile_name)
    profile.set_required_configs()

    # start firefox with specified profile
    Firefox.start("https://example.com/",
                  args.port,
                  profile_name,
                  ["-headless"])


    ###################################################
    client = RDPClient()
    client.connect(args.host, args.port)


    ###################################################
    ROOT = RootActor(client)
    root_actor_ids = ROOT.get_root()


    ###################################################
    DEVICE = DeviceActor(
        client, root_actor_ids["deviceActor"])


    ###################################################
    process_descriptors = ROOT.list_processes()
    for descriptor in process_descriptors:
        actor_id = descriptor["actor"]
        is_parent = descriptor["isParent"]

        PROCESS = ProcessActor(
            client, actor_id)
        target_ctx = PROCESS.get_target()

        CONSOLE = WebConsoleActor(
            client, target_ctx["consoleActor"])

        if (not is_parent):
            CONTENT_PROCESS = ContentProcessActor(
                client, target_ctx["actor"])


    ###################################################
    for descriptor in ROOT.list_addons():
        EXTENSION = WebExtensionActor(
            client, descriptor["actor"])


    ###################################################
    for descriptor in ROOT.list_workers():
        WORKER = WorkerActor(
            client, descriptor["actor"])


    ###################################################
    ADDONS = AddonsActor(
        client, root_actor_ids["addonsActor"])


    ###################################################
    tab_ctx = ROOT.list_tabs()[0]
    TAB = TabActor(client, tab_ctx["actor"])
    actor_ids = TAB.get_target()


    ###################################################
    WEB = BrowsingContextActor(
        client, actor_ids["actor"])
    web_context = WEB.attach()


    ###################################################
    CONSOLE = WebConsoleActor(
        client, actor_ids["consoleActor"])
    CONSOLE.start_listeners([])


    ###################################################
    THREAD = ThreadActor(
        client, web_context["threadActor"])
    THREAD.attach()


    ###################################################
    watcher_ctx = TAB.get_watcher()
    WATCHER = WatcherActor(
        client, watcher_ctx["actor"])
    WATCHER.watch_resources([
        WatcherActor.Resources.NETWORK_EVENT,
        WatcherActor.Resources.NETWORK_EVENT_STACKTRACE,
        WatcherActor.Resources.DOCUMENT_EVENT,
        WatcherActor.Resources.CACHE,
    ])


    ###################################################
    network_parent_ctx = WATCHER.get_network_parent_actor()
    NETWORK_PARENT = NetworkParentActor(
        client, network_parent_ctx["network"]["actor"])


    ###################################################
    NETWORK_CONTENT = NetworkContentActor(
        client, actor_ids["networkContentActor"])


    ###################################################
    WEB_EXT = WebExtensionInspectedWindowActor(
        client, actor_ids["webExtensionInspectedWindowActor"])


    ###################################################
    INSPECTOR = InspectorActor(
        client, actor_ids["inspectorActor"])


    ###################################################
    walker_ctx = INSPECTOR.get_walker()
    WALKER = WalkerActor(client, walker_ctx["actor"])


    ###################################################
    for descriptor in THREAD.sources():
        if (descriptor.get("actor", None) != None):
            SOURCE = SourceActor(client, descriptor["actor"])


    ###################################################
    PERFERENCE = PreferenceActor(
        client, root_actor_ids["preferenceActor"])


    ###################################################
    target_config_ctx = WATCHER.get_target_configuration_actor()
    TARGET_CONFIG = TargetConfigurationActor(
        client, target_config_ctx["actor"])


    ###################################################
    PERFORMANCE = PerformanceActor(
        client, actor_ids["performanceActor"])
    PERFORMANCE.connect({})


    ###################################################
    EVENT_SOURCE = EventSourceActor(
        client, actor_ids["eventSourceActor"])
    EVENT_SOURCE.start_listening()


    ###################################################
    WEBSOCKET = WebSocketActor(
        client, actor_ids["webSocketActor"])
    WEBSOCKET.start_listening()


    ###################################################
    SCREENSHOT = ScreenshotActor(
        client, root_actor_ids["screenshotActor"])


    ###################################################
    # -return a large enough string with 'evaluate_js_async()'
    # to trigger a longString response from server
    def on_evaluation_result(data: dict):
        result = data.get("result", data)
        if (not isinstance(result, dict)):
            return
        if (result.get("type", "") != "longString"):
            return
        STRING = StringActor(client, result["actor"])
        final_string_result = STRING.substring(
            0, result["length"])
        print(f"final_string_result(truncated): {final_string_result:5.5}...")

    client.add_event_listener(
        CONSOLE.actor_id, Events.WebConsole.EVALUATION_RESULT, on_evaluation_result)

    CONSOLE.evaluate_js_async("""
        (() => { 
            longString = '';
            for (let i = 0; i < 10000; i++) {
                longString += 'x';
            }
            return longString; 
        })();
    """)


    ###################################################
    # -register handler and trigger it by visiting a new page
    # -received actor IDs can be also stored temporary 
    # and initiated later
    def on_resource_available(data):
        resources = data["resources"]
        if (len(resources) <= 0):
            return
        resources = resources[0]
        if (resources["resourceType"] != "network-event"):
            return
        # the 'network_event_actor_id' represents a connection to a specified url or resource
        # after receiving it is possible to also receive updates for this ID with 'resource-updated-form'
        # if a host is visited, multiple connections are be established each with its own 'network_event_actor_id'
        # see also the network tab in the developer tools to see how it works
        network_event_actor_id = resources["actor"]
        resource_id = resources.get("resourceId", "N/A")
        url = resources.get("url", "N/A")
        NETWORK_EVENT = NetworkEventActor(
            client,
            network_event_actor_id)
        request = NETWORK_EVENT.get_request_headers()
        print(f"request headers:\n{json.dumps(request['headers'], indent=2)}")

    client.add_event_listener(
        watcher_ctx["actor"],
        Events.Watcher.RESOURCE_AVAILABLE_FORM,
        on_resource_available)

    WEB.navigate_to("https://example.com/")



    input()



if __name__ == "__main__":
    main()
