from geckordp.actors.actor import Actor


class MemoryActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/memory.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def attach(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "attach",
        })

    def detach(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "detach",
        })

    def get_state(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getState",
        })

    def take_census(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "takeCensus",
        })

    def start_recording_allocations(self, probability: float = None, max_log_length: int = None):
        if (probability is not None and (probability < 0.0 or probability > 1.0)):
            raise ValueError(
                "parameter 'probability' must be in range of 0.0 and 1.0")
        if (max_log_length is not None and max_log_length < 0.0):
            raise ValueError(
                "parameter 'max_log_length' cannot be negative")
        args = {
            "to": self.actor_id,
            "type": "startRecordingAllocations",
        }
        if (probability is not None or max_log_length is not None):
            args["options"] = {}
        if (probability is not None):
            args["options"]["probability"] = probability
        if (max_log_length is not None):
            args["options"]["maxLogLength"] = max_log_length
        
        return self.client.send_receive(args)

    def stop_recording_allocations(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "stopRecordingAllocations",
        })

    def get_allocations_settings(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getAllocationsSettings",
        })

    def get_allocations(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getAllocations",
        })

    def force_garbage_collection(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "forceGarbageCollection",
        })

    def force_cycle_collection(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "forceCycleCollection",
        })

    def measure(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "measure",
        })

    def resident_unique(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "residentUnique",
        })

    def save_heap_snapshot(self, boundaries: dict = None):
        """ 
            It seems like it will be handled automatically if no arguments are passed.
            A wireshark rdp session also doesn't pass any additional arguments nor any toggleable functions exists in the menu.
            I belive for many cases the snapshot should be ideal in the end.
            https://github.com/mozilla/gecko-dev/blob/d36cf98aa85f24ceefd07521b3d16b9edd2abcb7/devtools/shared/heapsnapshot/tests/xpcshell/test_SaveHeapSnapshot.js
            https://github.com/mozilla/gecko-dev/blob/d36cf98aa85f24ceefd07521b3d16b9edd2abcb7/devtools/server/performance/memory.js#L170
            https://github.com/mozilla/gecko-dev/blob/d36cf98aa85f24ceefd07521b3d16b9edd2abcb7/devtools/server/performance/memory.js#L170
        """
        args = {
            "to": self.actor_id,
            "type": "saveHeapSnapshot",
        }
        if (boundaries is not None):
            args["boundaries"] = boundaries
        return self.client.send_receive(args, "snapshotId")
