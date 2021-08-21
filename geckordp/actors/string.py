from geckordp.actors.actor import Actor


class StringActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/string.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def substring(self, start: int, end: int):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "substring",
            "start": start,
            "end": end,
        }, "substring")
