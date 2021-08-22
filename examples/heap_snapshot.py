""" This basic example demonstrates how to list all tabs.
"""
import base64
import datetime
import os
from pathlib import Path
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.heap_snapshot import HeapSnapshotActor
from geckordp.actors.memory import MemoryActor
from geckordp.profile import ProfileManager
from geckordp.firefox import Firefox


""" Uncomment to enable debug output
"""
#from geckordp.settings import GECKORDP
#GECKORDP.DEBUG = 1
#GECKORDP.DEBUG_REQUEST = 1
#GECKORDP.DEBUG_RESPONSE = 1


def screenshot(
        heap_snapshot_actor: HeapSnapshotActor,
        snapshot_id: str,
        file: Path) -> bool:
    path = Path(file).absolute()

    if (path.suffix != ".fxsnapshot"):
        raise RuntimeError("type must be .fxsnapshot")

    response = heap_snapshot_actor.transfer_heap_snapshot(snapshot_id)
    data = base64.b64decode(response["data"])
    assert response["data-decoded-size"] == len(data)

    if (file == ""):
        return False

    Path(os.path.dirname(path)).mkdir(
        parents=True, exist_ok=True)
    with open(str(path), "wb") as f:
        f.write(data)

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

    # initialize memory actor and retrieve the snapshot id
    memory = MemoryActor(client, actor_ids["memoryActor"])
    memory.attach()
    snapshot_id = memory.save_heap_snapshot()

    # initialize heap snapshot actor to transfer and create a heap snapshot file
    snapshot_actor = HeapSnapshotActor(
        client, root_actor_ids["heapSnapshotFileActor"])
    date_string = datetime.datetime.now().replace(
        microsecond=0).isoformat().replace(":", "").replace("-", "")
    snapshot_path = Path(f"Heap-{date_string}.fxsnapshot")
    info_url = "https://developer.mozilla.org/en-US/docs/Tools/Memory/Basic_operations#saving_and_loading_snapshots"
    if (screenshot(snapshot_actor, snapshot_id, snapshot_path)):
        print(
            f"successfull snapshot: {snapshot_path}\n\nTo load a snapshot, visit {info_url} for more information")
    else:
        print("failed to take a snapshot")

    input()


if __name__ == "__main__":
    main()
