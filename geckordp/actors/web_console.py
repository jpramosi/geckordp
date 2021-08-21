from enum import Enum
from typing import List
from geckordp.actors.actor import Actor


class WebConsoleActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/webconsole.js
    """

    class Listeners(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/8859fc390700d9f3ec4e5a4f38882e05eaf657bb/devtools/server/actors/webconsole.js#L616
            Listeners != Events
        """
        PAGE_ERROR = "PageError"
        CONSOLE_API = "ConsoleAPI"
        NETWORK_ACTIVITY = "NetworkActivity"
        FILE_ACTIVITY = "FileActivity"
        REFLOW_ACTIVITY = "ReflowActivity"
        CONTENT_PROCESS_MESSAGES = "ContentProcessMessages"
        DOCUMENT_EVENTS = "DocumentEvents"

    class MessageTypes(str, Enum):
        PAGE_ERROR = "PageError"
        CONSOLE_API = "ConsoleAPI"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start_listeners(self, listeners: List[Listeners]):
        nlisteners = []
        for listener in listeners:
            nlisteners.append(str(listener.value))
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "startListeners",
            "listeners": nlisteners,
        })

    def stop_listeners(self, listeners: List[Listeners]):
        nlisteners = []
        for listener in listeners:
            nlisteners.append(str(listener.value))
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "stopListeners",
            "listeners": nlisteners,
        })

    def get_cached_messages(self, message_types: List[MessageTypes]):
        nmessage_types = []
        for message_type in message_types:
            nmessage_types.append(str(message_type.value))
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getCachedMessages",
            "messageTypes": nmessage_types,
        })

    def evaluate_js_async(self, text: str, eager=False, frame_actor="", selected_node_actor="", inner_window_id=-1):
        args = {
            "to": self.actor_id,
            "type": "evaluateJSAsync",
            "text": text,
            "eager": eager,
        }
        if (frame_actor != ""):
            args["frameActor"] = frame_actor
        if (selected_node_actor != ""):
            args["selectedNodeActor"] = selected_node_actor
        if (inner_window_id != -1):
            args["innerWindowID"] = inner_window_id
        return self.client.send_receive(args)

    def autocomplete(self, text: str, cursor=0, frame_actor="",
                     selected_node_actor="", authorized_evaluations_json=None, expression_vars_json=None):
        if (authorized_evaluations_json is None):
            authorized_evaluations_json = {}
        if (expression_vars_json is None):
            expression_vars_json = {}
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "autocomplete",
            "text": text,
            "cursor": cursor,
            "frameActor": frame_actor,
            "selectedNodeActor": selected_node_actor,
            "authorizedEvaluations": authorized_evaluations_json,
            "expressionVars": expression_vars_json,
        })

    def clear_messages_cache(self):
        return self.client.send({
            "to": self.actor_id,
            "type": "clearMessagesCache",
        })

    def get_preferences(self, preferences: List[str] = None):
        # https://github.com/mozilla/gecko-dev/blob/d762ddd8ca9b9ec7138fac5b94585fa90c82a5e6/devtools/server/actors/webconsole.js#L1540
        if (preferences is None):
            preferences = [
                "NetworkMonitor.saveRequestAndResponseBodies",
                "NetworkMonitor.throttleData",
            ]
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getPreferences",
            "preferences": preferences,
        }, "preferences")

    def set_preferences(self, save_request_and_response_bodies=True):
        # https://github.com/mozilla/gecko-dev/blob/d762ddd8ca9b9ec7138fac5b94585fa90c82a5e6/devtools/server/actors/webconsole.js#L1540
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "setPreferences",
            "preferences": {
                "NetworkMonitor.saveRequestAndResponseBodies": save_request_and_response_bodies
            },
        }, "updated")

    def block_request(self, url: str):
        # https://github.com/mozilla/gecko-dev/blob/6178b9bfde68881523a8a30bbc0b78eac1f95159/devtools/server/actors/network-monitor/network-observer.js#L1029
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "blockRequest",
            "filter": {
                "url": url,
            },
        })

    def unblock_request(self, url: str):
        # https://github.com/mozilla/gecko-dev/blob/6178b9bfde68881523a8a30bbc0b78eac1f95159/devtools/server/actors/network-monitor/network-observer.js#L1044
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "unblockRequest",
            "filter": {
                "url": url,
            },
        })
