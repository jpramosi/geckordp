from geckordp.actors.actor import Actor


class ParentAccessibilityActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/accessibility.js#L263
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def bootstrap(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "bootstrap",
        })

    def enable(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "enable",
        })

    def disable(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "disable",
        })
