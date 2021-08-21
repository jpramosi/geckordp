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

    def get_watcher(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getWatcher"
        })
