from geckordp.actors.actor import Actor


class ProcessActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/descriptors/process.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_target(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getTarget",
        }, "process")

    def get_watcher(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getWatcher",
        })
