from geckordp.actors.actor import Actor


class AccessibilityActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/accessibility.js#L225
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_traits(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getTraits",
        }, "traits")
    
    def bootstrap(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "bootstrap",
        }, "state")

    def get_walker(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getWalker",
        }, "walker")

    def get_simulator(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getSimulator",
        }, "simulator")
