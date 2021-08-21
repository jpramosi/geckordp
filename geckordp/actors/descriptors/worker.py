from geckordp.actors.actor import Actor


class WorkerActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/descriptors/worker.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def attach(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "attach",
        })

    def detach(self):
        self.client.send({
            "to": self.actor_id,
            "type": "detach",
        })

    def get_target(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getTarget",
        })

    def push(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "push",
        })
