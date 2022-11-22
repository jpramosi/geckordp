from typing import Any, Dict
from geckordp.actors.actor import Actor


class ProcessActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/descriptors/process.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_target(self, is_browser_toolbox_fission: bool | None = None):
        args: Dict[str, Any] = {
            "to": self.actor_id,
            "type": "getTarget",
        }
        if is_browser_toolbox_fission is not None:
            args["isBrowserToolboxFission"] = is_browser_toolbox_fission
        return self.client.send_receive(args, "process")

    def get_watcher(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getWatcher",
        })
