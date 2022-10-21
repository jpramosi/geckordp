from enum import Enum
from typing import List
from geckordp.actors.actor import Actor


class WatcherActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/watcher.js
    """

    class Resources(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/6050205f3174fd24c2b6be11c69ecd788cd2b6b3/devtools/server/actors/resources/index.js
        """
        CONSOLE_MESSAGE = "console-message"
        CSS_CHANGE = "css-change"
        CSS_MESSAGE = "css-message"
        DOCUMENT_EVENT = "document-event"
        ERROR_MESSAGE = "error-message"
        PLATFORM_MESSAGE = "platform-message"
        NETWORK_EVENT = "network-event"
        STYLESHEET = "stylesheet"
        NETWORK_EVENT_STACKTRACE = "network-event-stacktrace"
        REFLOW = "reflow"
        SOURCE = "source"
        THREAD_STATE = "thread-state"
        SERVER_SENT_EVENT = "server-sent-event"
        WEBSOCKET = "websocket"
        # storage types
        CACHE_STORAGE = "Cache"
        COOKIE = "cookies"
        INDEXED_DB = "indexed-db"
        LOCAL_STORAGE = "local-storage"
        SESSION_STORAGE = "session-storage"
        # root types
        EXTENSIONS_BGSCRIPT_STATUS = "extensions-backgroundscript-status"

    class Targets(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/6178b9bfde68881523a8a30bbc0b78eac1f95159/devtools/server/actors/targets/index.js#L7
        """
        FRAME = "frame"
        PROCESS = "process"
        WORKER = "worker"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def watch_targets(self, target: Targets):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "watchTargets",
            "targetType": str(target.value),
        })

    def unwatch_targets(self, target: Targets):
        self.client.send({
            "to": self.actor_id,
            "type": "unwatchTargets",
            "targetType": str(target.value),
        })

    def get_parent_browsing_context_id(self, ctx_id: int):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getParentBrowsingContextID",
            "browsingContextID": ctx_id,
        })

    def watch_resources(self, resources: List[Resources]):
        objs = []
        for resource in resources:
            objs.append(str(resource.value))
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "watchResources",
            "resourceTypes": objs,
        })

    def unwatch_resources(self, resources: List[Resources]):
        objs = []
        for resource in resources:
            objs.append(str(resource.value))
        self.client.send({
            "to": self.actor_id,
            "type": "unwatchResources",
            "resourceTypes": objs,
        })

    def clear_resources(self, resources: List[Resources]):
        objs = []
        for resource in resources:
            objs.append(str(resource.value))
        self.client.send({
            "to": self.actor_id,
            "type": "clearResources",
            "resourceTypes": objs,
        })

    def get_network_parent_actor(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getNetworkParentActor",
        })

    def get_blackboxing_actor(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getBlackboxingActor",
        })

    def get_breakpoint_list_actor(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getBreakpointListActor",
        })

    def get_target_configuration_actor(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getTargetConfigurationActor",
        }, "configuration")

    def get_thread_configuration_actor(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getThreadConfigurationActor",
        }, "configuration")
