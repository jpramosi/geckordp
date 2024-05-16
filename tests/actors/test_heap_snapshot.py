# pylint: disable=unused-import
import base64
from time import sleep

import pytest

import tests.helpers.constants as constants
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.heap_snapshot import HeapSnapshotActor
from geckordp.actors.memory import MemoryActor
from geckordp.actors.root import RootActor
from geckordp.logger import log, logdict
from geckordp.rdp_client import RDPClient
from tests.helpers.utils import *


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    current_tab = root.current_tab()
    root_ids = root.get_root()
    tab = TabActor(cl, current_tab["actor"])
    actor_ids = tab.get_target()
    memory = MemoryActor(cl, actor_ids["memoryActor"])
    memory.attach()
    snapshot = HeapSnapshotActor(cl, root_ids["heapSnapshotFileActor"])
    return cl, snapshot, memory


def test_transfer_heap_snapshot():
    cl = None
    try:
        cl, snapshot, memory = init()
        snapshot_id = memory.save_heap_snapshot()

        # unable to find the command in RDP sessions
        # if you know how to resolve the issue, please let me know at https://github.com/jpramosi/geckordp/issues/new
        # {
        #     'to': 'server1.conn0.heapSnapshotFileActor5',
        #     'type': 'transferHeapSnapshot',
        #     'snapshotId': '3753'
        # }
        # {
        #     "from": "server1.conn0.heapSnapshotFileActor5",
        #     "error": "Error",
        #     "message": "ChromeUtils.importESModule: global option is required in DevTools distinct global",
        #     "fileName": "resource://devtools/shared/heapsnapshot/HeapSnapshotFileUtils.js",
        #     "lineNumber": 26,
        #     "columnNumber": 13
        # }

        # val = snapshot.transfer_heap_snapshot(snapshot_id)
        # assert val["data-size"] > 1000
        # decoded0 = base64.b64decode(val["data"])
        # # data is encoded with base64, however its string representation is in ascii
        # decoded1 = base64.decodebytes(bytes(val["data"], encoding="ascii"))
        # assert val["data-decoded-size"] == len(decoded0)
        # assert val["data-decoded-size"] == len(decoded1)
    finally:
        cl.disconnect()
