from geckordp.actors.actor import Actor


class NodeListActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/node.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def item(self, index: int):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "item",
            "item": index,
        })

    def items(self, start: int, end: int):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "items",
            "start": start,
            "end": end,
        })

    def release(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "release",
        })
