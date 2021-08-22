""" This basic example demonstrates how to list all tabs.
"""
import base64
import os
from pathlib import Path
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.screenshot import ScreenshotActor
from geckordp.profile import ProfileManager
from geckordp.firefox import Firefox


""" Uncomment to enable debug output
"""
#from geckordp.settings import GECKORDP
#GECKORDP.DEBUG = 1
#GECKORDP.DEBUG_REQUEST = 1
#GECKORDP.DEBUG_RESPONSE = 1


def screenshot(
        screenshot_actor: ScreenshotActor,
        browsing_context_id: int,
        file: Path,
        display_resolution=2,
        delay_sec=0) -> bool:
    path = Path(file).absolute()

    if (path.suffix != ".png"):
        raise RuntimeError("type must be .png")

    response = screenshot_actor.capture(
        browsing_context_id=browsing_context_id,
        copy_clipboard=False,
        dpr=display_resolution,
        delay_sec=delay_sec)

    value = response.get("value", None)
    if (not value):
        print("no value")
        return False

    data = value.get("data", None)
    if (not data):
        print("no image data")
        return False

    if (file == ""):
        return False

    Path(os.path.dirname(path)).mkdir(
        parents=True, exist_ok=True)
    with open(str(path), "wb") as f:
        f.write(base64.b64decode(
            str(data).replace("data:image/png;base64,", "")))

    return os.access(str(path), os.R_OK)


def main():
    # clone default profile to 'geckordp'
    pm = ProfileManager()
    profile_name = "geckordp"
    port = 6000
    pm.clone("default-release", profile_name)
    profile = pm.get_profile_by_name(profile_name)
    profile.set_required_configs()

    # start firefox with specified profile
    Firefox.start("https://example.com/",
                  port,
                  profile_name,
                  ["-headless"])

    # create client and connect to firefox
    client = RDPClient()
    client.connect("localhost", port)

    # initialize root
    root = RootActor(client)
    root_actor_ids = root.get_root()

    # get a single tab from tabs and retrieve its actor ID and context
    tabs = root.list_tabs()
    tab_descriptor = tabs[0]
    tab = TabActor(client, tab_descriptor["actor"])
    actor_ids = tab.get_target()
    browsing_context_id = actor_ids["browsingContextID"]

    # initialize screenshot actor and take a screenshot
    screenshot_actor = ScreenshotActor(
        client, root_actor_ids["screenshotActor"])
    screenshot_path = Path("screenshot.png")
    if (screenshot(screenshot_actor, browsing_context_id, screenshot_path)):
        print(f"successfull screenshot: {screenshot_path}")
    else:
        print("failed to take a screenshot")

    input()


if __name__ == "__main__":
    main()
