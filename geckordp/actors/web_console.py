from enum import Enum
from typing import List
from geckordp.actors.actor import Actor


class WebConsoleActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/webconsole.js
    """

    class Listeners(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/aa3ccd258b64abfd4c5ce56c1f512bc7f65b844c/devtools/server/actors/webconsole.js#LL548C17-L548C17
            Listeners != Events
        """
        PAGE_ERROR = "PageError"
        CONSOLE_API = "ConsoleAPI"
        FILE_ACTIVITY = "FileActivity"
        REFLOW_ACTIVITY = "ReflowActivity"
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

    def evaluate_js_async(
        self, text: str,
        eager=False,
        frame_actor="",
        selected_node_actor="",
        selected_object_actor="",
        inner_window_id=-1,
        mapped: dict | None = None
    ):
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
        if (selected_object_actor != ""):
            args["selectedObjectActor"] = selected_object_actor
        if (inner_window_id != -1):
            args["innerWindowID"] = inner_window_id
        if (mapped is not None):
            args["mapped"] = mapped
        return self.client.send_receive(args)

    def autocomplete(self, text: str, cursor=0, frame_actor="",
                     selected_node_actor="", authorized_evaluations_json: dict | None = None, expression_vars_json: dict | None = None):
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
