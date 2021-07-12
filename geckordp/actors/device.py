from geckordp.actors.actor import Actor


class DeviceActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/device.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_description(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getDescription",
        }, "value")
