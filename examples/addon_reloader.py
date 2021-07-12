""" This is a fully fledged example for installing or reloading 
    a temporary addon with automatic refresh on file changes.
"""
import argparse
import json
from urllib.parse import quote
from time import sleep
from pathlib import Path
from threading import Timer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent, EVENT_TYPE_CREATED
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.addon.addons import AddonsActor
from geckordp.actors.descriptors.web_extension import WebExtensionActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.targets.browsing_context import BrowsingContextActor


""" Uncomment to enable debug output
"""
#from geckordp.settings import GECKORDP
#GECKORDP.DEBUG = 1
#GECKORDP.DEBUG_REQUEST = 1
#GECKORDP.DEBUG_RESPONSE = 1


class DirectoryObserver(FileSystemEventHandler):

    def __init__(self, addon_actor: WebExtensionActor):
        self.__delay_sec = 0.7
        self.__addon = addon_actor
        self.__delay_timer = Timer(-1, self.reload)

    def on_any_event(self, event: FileSystemEvent):
        self.__delay_trigger(event)

    def __delay_trigger(self, event: FileSystemEvent):
        self.__delay_timer.cancel()
        self.__delay_timer = Timer(
            self.__delay_sec, self.reload, args=[event])
        self.__delay_timer.start()

    def reload(self, event: FileSystemEvent):
        response = self.__addon.reload()
        print(
            f"reload '{event.src_path}':\n{json.dumps(response, indent=2)}")


def main():
    # parse arguments
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--host", type=str, default="localhost",
                        help="The host to connect to")
    parser.add_argument("--port", type=int, default="6000",
                        help="The port to connect to")
    parser.add_argument("--addon", type=str, default="<addonpath>",
                        help="The addon path")
    parser.add_argument("--list", action="store_true", help="List all addons")
    parser.add_argument("--visitaddon", action="store_true",
                        help="Visit the debug page of the addon")
    args, _ = parser.parse_known_args()

    # create client and connect to firefox
    client = RDPClient()
    client.connect(args.host, args.port)

    # get global actors IDs from root actor
    root = RootActor(client)
    root_actor_ids = root.get_root()

    # if user just wants to know the list of addons, print it and return
    if (args.list):
        print(json.dumps(root.list_addons(), indent=2))
        return

    # check addon path
    addon_path = Path(args.addon).absolute()
    if (not addon_path.exists()):
        print(f"addon path {addon_path} doesn't exist")
        return
    addon_path = str(addon_path)

    # install temporary addon if not found, else set flag for reloading it
    addons = [addon for addon in root.list_addons()
              if addon_path in addon.get("url", "")]
    reload_now = False
    if (len(addons) == 0):
        print(f"install temporary addon from '{addon_path}'")
        response = AddonsActor(
            client, root_actor_ids["addonsActor"]).install_temporary_addon(addon_path)
        addon_id = response.get("id", None)
        if (addon_id == None):
            print(
                f"addon could not be loaded:\n'{json.dumps(response, indent=2)}'")
            return
        print(f"addon '{addon_id}' loaded")
    else:
        print("addon already installed, start reloading it")
        reload_now = True

    # check whether addon can be found via list_addons()
    addons = [addon for addon in root.list_addons()
              if addon_path in addon.get("url", "")]
    if (len(addons) == 0):
        print("addon wasn't found in list")
        return

    # retrieve the ID of the found addon and start the file watcher
    event_handler = DirectoryObserver(
        WebExtensionActor(client, addons[0]["actor"]))
    observer = Observer()
    observer.schedule(
        event_handler, path=addon_path, recursive=True)
    observer.start()

    # reload now if flag was set
    if (reload_now):
        ev = FileSystemEvent(addon_path)
        ev.event_type = EVENT_TYPE_CREATED
        ev.is_directory = True
        event_handler.reload(ev)

    # visit extension page with debugger
    if (args.visitaddon):
        tab = TabActor(client, root.current_tab()["actor"])
        tab_actor_ids = tab.get_target()
        web = BrowsingContextActor(client, tab_actor_ids["actor"])
        web.attach()
        web.navigate_to(
            f"about:devtools-toolbox?id={quote(addons[0]['id'])}&type=extension")

    # sleep and let the observer handle file updates
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        client.disconnect()


if __name__ == "__main__":
    main()
