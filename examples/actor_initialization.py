""" This example demonstrates the initialization procedure of every available actor.
"""
# pylint: disable=unused-variable
# pylint: disable=invalid-name
import argparse
from concurrent.futures import Future
import json
from geckordp.rdp_client import RDPClient
from geckordp.actors.events import Events
from geckordp.actors.accessibility.accessibility import AccessibilityActor
from geckordp.actors.accessibility.accessible import AccessibleActor
from geckordp.actors.accessibility.accessible_walker import AccessibleWalkerActor
from geckordp.actors.accessibility.parent_accessibility import ParentAccessibilityActor
from geckordp.actors.accessibility.simulator import SimulatorActor
from geckordp.actors.addon.addons import AddonsActor
from geckordp.actors.addon.web_extension_inspected_window import WebExtensionInspectedWindowActor
from geckordp.actors.descriptors.process import ProcessActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.descriptors.web_extension import WebExtensionActor
from geckordp.actors.descriptors.worker import WorkerActor
from geckordp.actors.device import DeviceActor
from geckordp.actors.heap_snapshot import HeapSnapshotActor
from geckordp.actors.inspector import InspectorActor
from geckordp.actors.memory import MemoryActor
from geckordp.actors.network_content import NetworkContentActor
from geckordp.actors.network_event import NetworkEventActor
from geckordp.actors.network_parent import NetworkParentActor
from geckordp.actors.node import NodeActor
from geckordp.actors.node_list import NodeListActor
from geckordp.actors.preference import PreferenceActor
from geckordp.actors.root import RootActor
from geckordp.actors.screenshot import ScreenshotActor
from geckordp.actors.source import SourceActor
from geckordp.actors.storage import CacheStorageActor
from geckordp.actors.storage import CookieStorageActor
from geckordp.actors.storage import IndexedDBStorageActor
from geckordp.actors.storage import LocalStorageActor
from geckordp.actors.storage import SessionStorageActor
from geckordp.actors.string import StringActor
from geckordp.actors.target_configuration import TargetConfigurationActor
from geckordp.actors.targets.content_process import ContentProcessActor
from geckordp.actors.targets.window_global import WindowGlobalActor
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
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--host", type=str, default="localhost",
                        help="The host to connect to")
    parser.add_argument("--port", type=int, default="6000",
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

    # RDPClient
    ###################################################
    client = RDPClient()
    client.connect(args.host, args.port)

    # RootActor
    ###################################################
    ROOT = RootActor(client)
    root_actor_ids = ROOT.get_root()

    # DeviceActor
    ###################################################
    DEVICE = DeviceActor(
        client, root_actor_ids["deviceActor"])

    # ContentProcessActor
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

    # WebExtensionActor
    ###################################################
    for descriptor in ROOT.list_addons():
        EXTENSION = WebExtensionActor(
            client, descriptor["actor"])

    # WorkerActor
    ###################################################
    for descriptor in ROOT.list_workers():
        WORKER = WorkerActor(
            client, descriptor["actor"])

    # AddonsActor
    ###################################################
    ADDONS = AddonsActor(
        client, root_actor_ids["addonsActor"])

    # TabActor
    ###################################################
    tab_ctx = ROOT.list_tabs()[0]
    TAB = TabActor(
        client, tab_ctx["actor"])
    actor_ids = TAB.get_target()

    # AccessibilityActor
    ###################################################
    ACCESSIBILITY = AccessibilityActor(
        client, actor_ids["accessibilityActor"])
    ACCESSIBILITY.bootstrap()

    # ParentAccessibilityActor
    ###################################################
    PARENT_ACCESSIBILITY = ParentAccessibilityActor(
        client, root_actor_ids["parentAccessibilityActor"])
    PARENT_ACCESSIBILITY.bootstrap()
    PARENT_ACCESSIBILITY.enable()

    # AccessibleWalkerActor
    ###################################################
    ACCESSIBILITY_WALKER = AccessibleWalkerActor(
        client, ACCESSIBILITY.get_walker()["actor"])

    # AccessibleActor
    ###################################################
    accessible_children = ACCESSIBILITY_WALKER.children()
    ACCESSIBLE = AccessibleActor(
        client, accessible_children[0]["actor"])

    # SimulatorActor
    ###################################################
    simulator = SimulatorActor(
        client, ACCESSIBILITY.get_simulator())

    # WindowGlobalActor
    ###################################################
    WEB = WindowGlobalActor(
        client, actor_ids["actor"])

    # WebConsoleActor
    ###################################################
    CONSOLE = WebConsoleActor(
        client, actor_ids["consoleActor"])
    CONSOLE.start_listeners([])

    # ThreadActor
    ###################################################
    THREAD = ThreadActor(
        client, actor_ids["threadActor"])
    THREAD.attach()

    # WatcherActor
    ###################################################
    watcher_ctx = TAB.get_watcher()
    WATCHER = WatcherActor(
        client, watcher_ctx["actor"])
    WATCHER.watch_resources([
        WatcherActor.Resources.NETWORK_EVENT,
        WatcherActor.Resources.NETWORK_EVENT_STACKTRACE,
        WatcherActor.Resources.DOCUMENT_EVENT,
    ])

    # NetworkParentActor
    ###################################################
    network_parent_ctx = WATCHER.get_network_parent_actor()
    NETWORK_PARENT = NetworkParentActor(
        client, network_parent_ctx["network"]["actor"])

    # NetworkContentActor
    ###################################################
    NETWORK_CONTENT = NetworkContentActor(
        client, actor_ids["networkContentActor"])

    # WebExtensionInspectedWindowActor
    ###################################################
    WEB_EXT = WebExtensionInspectedWindowActor(
        client, actor_ids["webExtensionInspectedWindowActor"])

    # InspectorActor
    ###################################################
    INSPECTOR = InspectorActor(
        client, actor_ids["inspectorActor"])

    # WalkerActor
    ###################################################
    walker_ctx = INSPECTOR.get_walker()
    WALKER = WalkerActor(client, walker_ctx["actor"])

    # NodeListActor
    ###################################################
    document = WALKER.document()
    dom_node_list = WALKER.query_selector_all(document["actor"], "body h1")
    NODE_LIST = NodeListActor(client, dom_node_list["actor"])

    # NodeActor
    ###################################################
    node_element = WALKER.query_selector(document["actor"], "body h1")["node"]
    NODE = NodeActor(client, node_element["actor"])

    # MemoryActor
    ###################################################
    MEMORY = MemoryActor(client, actor_ids["memoryActor"])
    MEMORY.attach()

    # SourceActor
    ###################################################
    for descriptor in THREAD.sources():
        if (descriptor.get("actor", None) is not None):
            SOURCE = SourceActor(client, descriptor["actor"])

    # HeapSnapshotActor
    ###################################################
    SNAPSHOT = HeapSnapshotActor(
        client, root_actor_ids["heapSnapshotFileActor"])

    # PreferenceActor
    ###################################################
    PERFERENCE = PreferenceActor(
        client, root_actor_ids["preferenceActor"])

    # TargetConfigurationActor
    ###################################################
    target_config_ctx = WATCHER.get_target_configuration_actor()
    TARGET_CONFIG = TargetConfigurationActor(
        client, target_config_ctx["actor"])

    # CacheStorageActor
    ###################################################
    cache_resource = {}
    cache_fut = Future()

    async def on_cache_resource(data: dict):
        resources = data.get("resources", [])
        for resource in resources:
            if ("Cache" in resource.get("actor", "")):
                cache_fut.set_result(resource)

    client.add_event_listener(
        WEB.actor_id, Events.Watcher.RESOURCE_AVAILABLE_FORM, on_cache_resource)

    WATCHER.watch_targets(WatcherActor.Targets.FRAME)
    WATCHER.watch_resources([WatcherActor.Resources.CACHE_STORAGE])

    cache_resource = cache_fut.result(3.0)

    cache_storage_id = cache_resource.get("actor", "")
    CACHE = CacheStorageActor(client, cache_storage_id)

    # CookieStorageActor
    ###################################################
    cookie_resource = {}
    cookie_fut = Future()

    async def on_cookie_resource(data: dict):
        resources = data.get("resources", [])
        for resource in resources:
            if ("cookie" in resource.get("actor", "")):
                cookie_fut.set_result(resource)

    client.add_event_listener(
        WATCHER.actor_id, Events.Watcher.RESOURCE_AVAILABLE_FORM, on_cookie_resource)

    WATCHER.watch_targets(WatcherActor.Targets.FRAME)
    WATCHER.watch_resources([WatcherActor.Resources.COOKIE])

    cookie_resource = cookie_fut.result(3.0)

    cookie_storage_id = cookie_resource.get("actor", "")
    COOKIE = CookieStorageActor(client, cookie_storage_id)

    # ExtensionStorageActor
    ###################################################
    """ At the moment not possible. 
    See also tests/actors/test_storage_extension. """

    # IndexedDBStorageActor
    ###################################################
    indexed_resource = {}
    indexed_fut = Future()

    async def on_indexed_resource(data: dict):
        resources = data.get("resources", [])
        for resource in resources:
            if ("indexedDB" in resource.get("actor", "")):
                indexed_fut.set_result(resource)

    client.add_event_listener(
        WATCHER.actor_id, Events.Watcher.RESOURCE_AVAILABLE_FORM, on_indexed_resource)

    WATCHER.watch_targets(WatcherActor.Targets.FRAME)
    WATCHER.watch_resources([WatcherActor.Resources.INDEXED_DB])

    indexed_resource = indexed_fut.result(3.0)

    indexed_storage_id = indexed_resource.get("actor", "")
    INDEXED = IndexedDBStorageActor(client, indexed_storage_id)

    # LocalStorageActor
    ###################################################
    local_resource = {}
    local_fut = Future()

    async def on_local_resource(data: dict):
        resources = data.get("resources", [])
        for resource in resources:
            if ("local" in resource.get("actor", "")):
                local_fut.set_result(resource)

    window_global_actor = actor_ids["actor"]
    client.add_event_listener(
        window_global_actor, Events.Watcher.RESOURCE_AVAILABLE_FORM, on_local_resource)

    WATCHER.watch_targets(WatcherActor.Targets.FRAME)
    WATCHER.watch_resources([WatcherActor.Resources.LOCAL_STORAGE])

    local_resource = local_fut.result(3.0)

    local_storage_id = local_resource.get("actor", "")
    LOCAL = LocalStorageActor(client, local_storage_id)

    # SessionStorageActor
    ###################################################
    session_resource = {}
    session_fut = Future()

    async def on_session_resource(data: dict):
        resources = data.get("resources", [])
        for resource in resources:
            if ("session" in resource.get("actor", "")):
                session_fut.set_result(resource)

    window_global_actor = actor_ids["actor"]
    client.add_event_listener(
        window_global_actor, Events.Watcher.RESOURCE_AVAILABLE_FORM, on_session_resource)

    WATCHER.watch_targets(WatcherActor.Targets.FRAME)
    WATCHER.watch_resources([WatcherActor.Resources.SESSION_STORAGE])

    session_resource = session_fut.result(3.0)

    session_storage_id = session_resource.get("actor", "")
    SESSION = SessionStorageActor(client, session_storage_id)

    # WebSocketActor
    ###################################################
    WEBSOCKET = WebSocketActor(
        client, actor_ids["webSocketActor"])
    WEBSOCKET.start_listening()

    # ScreenshotActor
    ###################################################
    SCREENSHOT = ScreenshotActor(
        client, root_actor_ids["screenshotActor"])

    # StringActor
    ###################################################

    def on_evaluation_result(data: dict):
        """ 
        - return a large enough string with 'evaluate_js_async()'
        to trigger a longString response from server 
        """
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

    # NetworkEventActor
    ###################################################

    def on_resource_available(data):
        resources = data["resources"]
        if (len(resources) <= 0):
            return
        resources = resources[0]
        if (resources["resourceType"] != "network-event"):
            return
        """ 
        the 'network_event_actor_id' represents a connection to a specified url or resource
        after receiving it is possible to also receive updates for this ID with 'resource-updated-form'
        if a host is visited, multiple connections are be established each with its own 'network_event_actor_id'
        see also the network tab in the developer tools to see how it works
        """
        network_event_actor_id = resources["actor"]
        resource_id = resources.get("resourceId", "N/A")
        url = resources.get("url", "N/A")
        NETWORK_EVENT = NetworkEventActor(
            client,
            network_event_actor_id)
        request = NETWORK_EVENT.get_request_headers()
        print(f"request headers:\n{json.dumps(request['headers'], indent=2)}")

    """ 
    - register handler and trigger it by visiting a new page
    - received actor IDs can be also stored temporary
        and initiated later
    """
    client.add_event_listener(
        watcher_ctx["actor"],
        Events.Watcher.RESOURCE_AVAILABLE_FORM,
        on_resource_available)

    WEB.navigate_to("https://example.com/")

    input()


if __name__ == "__main__":
    main()
