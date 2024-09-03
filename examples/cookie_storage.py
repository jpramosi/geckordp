""" This example demonstrates how to access cookie storage data.
"""

import argparse
import json
import uuid
from concurrent.futures import Future

from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.events import Events
from geckordp.actors.resources import Resources
from geckordp.actors.root import RootActor
from geckordp.actors.storage import CookieStorageActor
from geckordp.actors.watcher import WatcherActor
from geckordp.firefox import Firefox
from geckordp.profile import ProfileManager
from geckordp.rdp_client import RDPClient

""" Uncomment to enable debug output
"""
# from geckordp.settings import GECKORDP
# GECKORDP.DEBUG = 1
# GECKORDP.DEBUG_REQUEST = 1
# GECKORDP.DEBUG_RESPONSE = 1


def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--host", type=str, default="localhost", help="The host to connect to"
    )
    parser.add_argument(
        "--port", type=int, default="6000", help="The port to connect to"
    )
    args, _ = parser.parse_known_args()

    # clone default profile to 'geckordp'
    pm = ProfileManager()
    profile_name = "geckordp"
    pm.clone("default-release", profile_name)
    profile = pm.get_profile_by_name(profile_name)
    profile.set_required_configs()

    # start firefox with specified profile
    Firefox.start(
        "https://samesitetest.com/cookies/set", args.port, profile_name, ["-headless"]
    )

    # create client and connect to firefox
    client = RDPClient()
    client.connect(args.host, args.port)

    # initialize root
    root = RootActor(client)

    # get a single tab from tabs and retrieve its actor ID
    tabs = root.list_tabs()
    tab_descriptor = tabs[0]
    tab = TabActor(client, tab_descriptor["actor"])

    # initialize watcher
    watcher_ctx = tab.get_watcher()
    watcher = WatcherActor(client, watcher_ctx["actor"])

    ###################################################
    # This procedure will retrieve the cookie resource
    # which contains the actor and hosts

    # cookie data
    cookie_resource = {}
    cookie_fut = Future()

    # receive here resource data of cookie storage
    async def on_cookie_resource(data: dict):
        array = data.get("array", [])
        for obj in array:
            obj: list
            for i, item in enumerate(obj):
                item: str | list
                if isinstance(item, str) and "cookies" in item:
                    # obj[i + 1] = next item in array
                    for cookie_obj in obj[i + 1]:
                        cookie_obj: dict
                        if "cookie" in cookie_obj.get("actor", ""):
                            # just get the first one for example purposes
                            try:
                                cookie_fut.set_result(cookie_obj)
                            except:
                                pass
                            break

    # add event listener with the specified watcher actor ID
    # - watcher.actor_id = Resources.COOKIE
    # - watcher.actor_id = Resources.INDEXED
    # - actor_ids["actor"] = Resources.CACHE_STORAGE
    # - actor_ids["actor"] = Resources.LOCAL_STORAGE
    # - actor_ids["actor"] = Resources.SESSION_STORAGE
    client.add_event_listener(
        watcher.actor_id, Events.Watcher.RESOURCES_AVAILABLE_ARRAY, on_cookie_resource
    )

    # set frame as target and notify server to watch for cookie resources
    watcher.watch_targets(WatcherActor.Targets.FRAME)
    watcher.watch_resources([Resources.COOKIE])

    # wait for resource to be available within 3 seconds
    cookie_resource = cookie_fut.result(3.0)

    # get data from resource
    hosts = cookie_resource.get("hosts", {})
    cookie_storage_actor_id = cookie_resource.get("actor", "")
    cookie_actor = CookieStorageActor(client, cookie_storage_actor_id)

    # get specific url from hosts which will be used to retrieve storage objects
    # the first host can also be used, since only cookies will be shown for the current web page
    host = ""
    for h, _ in hosts.items():
        if "samesitetest.com" in h:
            host = h
    if host == "":
        raise RuntimeError("host not found")

    # retrieve the actual cookie list for this host
    cookie_objects = cookie_actor.get_store_objects(host, options={"sessionString": ""})
    print(json.dumps(cookie_objects, indent=2))

    ###################################################
    # This procedure will:
    # - initialize a future callback
    # - edit existing cookie
    # - add & edit cookie
    # - print an updated version of the cookies

    # future to wait for updates
    stores_update_fut = Future()

    # receive here storage updates
    async def on_stores_update(data: dict):
        stores_update_fut.set_result(data.get("data", {}))

    # add event listener with the specified watcher actor ID
    client.add_event_listener(
        cookie_storage_actor_id, Events.Storage.STORES_UPDATE, on_stores_update
    )

    def get_cookie_by_name(cookies: list, name: str) -> dict:
        """Helper function"""
        cname = name.lower()
        for cookie in cookies:
            cookie_name = cookie.get("name", "").lower()
            if cookie_name == cname:
                return cookie
        return {}

    ###################################################
    # edit existing cookie

    # get the cookie 'StrictCookie'
    cookie = get_cookie_by_name(cookie_objects.get("data", {}), "StrictCookie")

    # change a field its content with the name 'value' to 'my_new_value'
    cookie_actor.edit_item(
        host, "value", cookie.get("value", ""), "my_new_value", cookie
    )

    # wait for storage update and update cookie list
    _data = stores_update_fut.result(1.0)
    cookie_objects = cookie_actor.get_store_objects(host, options={"sessionString": ""})

    ###################################################
    # add & edit cookie
    #
    # usually if the cookie list is modified,
    # one needs to update the local cookie list
    #
    # at this example, 'cookie_objects' will be updated with futures
    # after modifications

    # generate random guid and add cookie item
    rnd_guid = "{" + str(uuid.uuid4()) + "}"
    stores_update_fut = Future()
    cookie_actor.add_item(rnd_guid, host)
    _data = stores_update_fut.result(1.0)
    cookie_objects = cookie_actor.get_store_objects(host, options={"sessionString": ""})

    # find cookie by its guid
    cookie = get_cookie_by_name(cookie_objects.get("data", {}), rnd_guid)

    # edit added cookie
    stores_update_fut = Future()
    cookie_actor.edit_item(host, "name", cookie.get("name", ""), "MyNewCookie", cookie)
    _data = stores_update_fut.result(1.0)
    cookie_objects = cookie_actor.get_store_objects(host, options={"sessionString": ""})

    # find cookie by its name instead of guid
    cookie = get_cookie_by_name(cookie_objects.get("data", {}), "MyNewCookie")

    # change the value of cookie
    stores_update_fut = Future()
    cookie_actor.edit_item(
        host, "value", cookie.get("value", ""), "my_new_cookie_value", cookie
    )
    _data = stores_update_fut.result(1.0)
    cookie_objects = cookie_actor.get_store_objects(host, options={"sessionString": ""})

    # print updated version storage objects
    print(json.dumps(cookie_objects, indent=2))

    input()


if __name__ == "__main__":
    main()
