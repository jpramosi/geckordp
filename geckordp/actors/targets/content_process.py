from geckordp.actors.actor import Actor


class ContentProcessActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/targets/content-process.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def list_workers(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "listWorkers",
        }, "workers")

    def pause_matching_service_workers(self, origin = ""):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "pauseMatchingServiceWorkers",
            "origin": origin,
        })
