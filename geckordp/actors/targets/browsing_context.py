from geckordp.actors.actor import Actor


class BrowsingContextActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/targets/browsing-context.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def attach(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "attach",
        })

    def detach(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "detach",
        })

    def ensure_css_error_reporting_enabled(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "ensureCSSErrorReportingEnabled",
        })

    def focus(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "focus",
        })

    def go_forward(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "goForward",
        })

    def go_back(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "goBack",
        })

    def reload(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "reload",
        })

    def navigate_to(self, url : str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "navigateTo",
            "url": url,
        })

    def switch_to_frame(self, window_id : str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "switchToFrame",
            "windowId": window_id,
        })

    def list_frames(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "listFrames",
        })["frames"]

    def list_workers(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "listWorkers",
        })

    def log_in_page(self, text = "", category = "", flags = ""):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "logInPage",
            "text": text,
            "category": category,
            "flags": flags,
        })
