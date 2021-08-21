from geckordp.actors.actor import Actor


class WebExtensionActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/descriptors/webextension.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def reload(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "reload"
        })

    def connect(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "connect"
        })

    def get_target(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getTarget"
        })
