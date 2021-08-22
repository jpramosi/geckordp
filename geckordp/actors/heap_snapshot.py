from geckordp.actors.actor import Actor


class HeapSnapshotActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/heap-snapshot-file.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def transfer_heap_snapshot(self, snapshot_id: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "transferHeapSnapshot",
            "snapshotId": snapshot_id,
        })
