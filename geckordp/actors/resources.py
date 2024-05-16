from enum import Enum
from typing import List

from geckordp.actors.actor import Actor


class Resources(str, Enum):
    """
    On some actors only a few resource types may be working.
    https://github.com/mozilla/gecko-dev/blob/master/devtools/server/actors/resources/index.js
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


class ResourceActor(Actor):
    """Internal inofficial actor"""

    def watch_resources(self, resources: List[Resources]):
        objs = []
        for resource in resources:
            objs.append(str(resource.value))
        return self.client.send_receive(
            {
                "to": self.actor_id,
                "type": "watchResources",
                "resourceTypes": objs,
            }
        )

    def unwatch_resources(self, resources: List[Resources]):
        objs = []
        for resource in resources:
            objs.append(str(resource.value))
        self.client.send(
            {
                "to": self.actor_id,
                "type": "unwatchResources",
                "resourceTypes": objs,
            }
        )

    def clear_resources(self, resources: List[Resources]):
        objs = []
        for resource in resources:
            objs.append(str(resource.value))
        self.client.send(
            {
                "to": self.actor_id,
                "type": "clearResources",
                "resourceTypes": objs,
            }
        )
