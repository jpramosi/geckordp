from geckordp.actors.actor import Actor


class PerformanceActor(Actor):
    # todo: add missing functions
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/performance.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def connect(self, args: dict):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "connect",
            "options": args,
        })
