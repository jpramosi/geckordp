from geckordp.actors.actor import Actor


class WebSocketActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/websocket.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start_listening(self):
        return self.client.request({
            "to": self.actor_id,
            "type": "startListening",
        })

    def stop_listening(self):
        return self.client.request({
            "to": self.actor_id,
            "type": "stopListening",
        })
