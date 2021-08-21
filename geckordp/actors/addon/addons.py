from geckordp.actors.actor import Actor


class AddonsActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/addon/addons.js
        https://github.com/mozilla/web-ext/blob/master/src/firefox/remote.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def install_temporary_addon(self, addon_path : str):
        response = self.client.send_receive({
            "to": self.actor_id,
            "type": "installTemporaryAddon",
            "addonPath": addon_path,
        })
        return response.get("addon", response)
