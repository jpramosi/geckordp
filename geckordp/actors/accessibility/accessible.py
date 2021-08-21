from geckordp.actors.actor import Actor


class AccessibleActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/accessibility.js#L46
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def audit(self, options: dict = None):
        if (options is None):
            options = {}
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "audit",
            "options": options,
        })

    def children(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "children",
        }, "children")

    def get_relations(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getRelations",
        }, "relations")

    def hydrate(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "hydrate",
        }, "properties")

    def snapshot(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "snapshot",
        }, "snapshot")
