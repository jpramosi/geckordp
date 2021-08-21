from geckordp.actors.actor import Actor


class PerformanceActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/performance.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def connect(self, options: dict = None):
        if (options is None):
            options = {}
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "connect",
            "options": options,
        })

    def can_currently_record(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "canCurrentlyRecord",
        })

    def start_recording(self,
                        with_markers=True,
                        with_ticks=True,
                        with_memory=False,
                        with_frames=True,
                        with_gc_events=True,
                        with_allocations=False,
                        allocations_sample_probability=0.05,
                        allocations_max_log_length=125000,
                        buffer_size=10000000,
                        sample_frequency=1000
                        ):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "startRecording",
            "options": {
                "withMarkers": with_markers,
                "withTicks": with_ticks,
                "withMemory": with_memory,
                "withFrames": with_frames,
                "withGCEvents": with_gc_events,
                "withAllocations": with_allocations,
                "allocationsSampleProbability": allocations_sample_probability,
                "allocationsMaxLogLength": allocations_max_log_length,
                "bufferSize": buffer_size,
                "sampleFrequency": sample_frequency,
            },
        }, "recording")

    def stop_recording(self, performance_recording_actor=""):
        # required actor is received on 'start_recording()'
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "stopRecording",
            "options": performance_recording_actor
        }, "recording")

    def is_recording(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "isRecording",
        }, "isRecording")

    def get_recordings(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getRecordings",
        }, "recordings")

    def get_configuration(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getConfiguration",
        }, "config")

    def set_profiler_status_interval(self, interval: int):
        return self.client.send({
            "to": self.actor_id,
            "type": "setProfilerStatusInterval",
            "interval": interval,
        })
