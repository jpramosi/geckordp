""" This example demonstrates how to execute javascript code and retrieve the results.
"""
import argparse
import json
from geckordp.rdp_client import RDPClient
from geckordp.actors.events import Events
from geckordp.actors.root import RootActor
from geckordp.actors.web_console import WebConsoleActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.targets.browsing_context import BrowsingContextActor
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

    # create client and connect to firefox
    client = RDPClient()
    client.connect(args.host, args.port)

    # initialize root
    root = RootActor(client)

    # get a single tab from tabs and retrieve its actor ID
    tabs = root.list_tabs()
    tab_descriptor = tabs[0]
    tab = TabActor(client, tab_descriptor["actor"])
    actor_ids = tab.get_target()

    # receive here evaluation results
    async def on_evaluation_result(data: dict):
        # beautify python dictionary and print it
        print(json.dumps(data, indent=2))

    # initialize and attach context to receive evaluation results
    ctx_actor_id = actor_ids["actor"]
    web = BrowsingContextActor(
        client, ctx_actor_id)
    _web_context = web.attach()

    # add event listener with the specified console actor ID
    console_actor_id = actor_ids["consoleActor"]
    client.add_event_listener(
        console_actor_id, Events.WebConsole.EVALUATION_RESULT, on_evaluation_result)

    # initialize console and start listening
    console = WebConsoleActor(
        client, console_actor_id)
    console.start_listeners([])

    # execute javascript on example page
    console.evaluate_js_async("""
        (() => { return document.title; })();
    """)

    input()


if __name__ == "__main__":
    main()
