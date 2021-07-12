""" This basic example demonstrates how to list all tabs.
"""
import json
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.profile import ProfileManager
from geckordp.firefox import Firefox


""" Uncomment to enable debug output
"""
#from geckordp.settings import GECKORDP
#GECKORDP.DEBUG = 1
#GECKORDP.DEBUG_REQUEST = 1
#GECKORDP.DEBUG_RESPONSE = 1


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

    # get a list of tabs
    tabs = root.list_tabs()
    print(json.dumps(tabs, indent=2))

    input()

if __name__ == "__main__":
    main()
