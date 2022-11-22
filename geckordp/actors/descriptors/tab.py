from typing import Any, Dict
from geckordp.actors.actor import Actor


class TabActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/descriptors/tab.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_target(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getTarget"
        }, "frame")

    def get_favicon(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getFavicon"
        }, "favicon")

    def get_watcher(self, is_server_target_switching_enabled: bool | None = None, is_popup_debugging_enabled: bool | None = None):
        args: Dict[str, Any] = {
            "to": self.actor_id,
            "type": "getWatcher",
            "isServerTargetSwitchingEnabled": is_server_target_switching_enabled,
            "isPopupDebuggingEnabled": is_popup_debugging_enabled,
        }
        if is_server_target_switching_enabled is not None:
            args["isServerTargetSwitchingEnabled"] = is_server_target_switching_enabled
        if is_popup_debugging_enabled is not None:
            args["isPopupDebuggingEnabled"] = is_popup_debugging_enabled
        return self.client.send_receive(args)
