from enum import Enum

from geckordp.actors.resources import ResourceActor


class WatcherActor(ResourceActor):
    """https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/watcher.js"""

    class Targets(str, Enum):
        """https://github.com/mozilla/gecko-dev/blob/6178b9bfde68881523a8a30bbc0b78eac1f95159/devtools/server/actors/targets/index.js#L7"""

        FRAME = "frame"
        PROCESS = "process"
        WORKER = "worker"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def watch_targets(self, target: Targets):
        return self.client.send_receive(
            {
                "to": self.actor_id,
                "type": "watchTargets",
                "targetType": str(target.value),
            }
        )

    def unwatch_targets(self, target: Targets):
        self.client.send(
            {
                "to": self.actor_id,
                "type": "unwatchTargets",
                "targetType": str(target.value),
            }
        )

    def get_parent_browsing_context_id(self, ctx_id: int):
        return self.client.send_receive(
            {
                "to": self.actor_id,
                "type": "getParentBrowsingContextID",
                "browsingContextID": ctx_id,
            }
        )

    def get_network_parent_actor(self):
        return self.client.send_receive(
            {
                "to": self.actor_id,
                "type": "getNetworkParentActor",
            }
        )

    def get_blackboxing_actor(self):
        return self.client.send_receive(
            {
                "to": self.actor_id,
                "type": "getBlackboxingActor",
            }
        )

    def get_breakpoint_list_actor(self):
        return self.client.send_receive(
            {
                "to": self.actor_id,
                "type": "getBreakpointListActor",
            }
        )

    def get_target_configuration_actor(self):
        return self.client.send_receive(
            {
                "to": self.actor_id,
                "type": "getTargetConfigurationActor",
            },
            "configuration",
        )

    def get_thread_configuration_actor(self):
        return self.client.send_receive(
            {
                "to": self.actor_id,
                "type": "getThreadConfigurationActor",
            },
            "configuration",
        )
