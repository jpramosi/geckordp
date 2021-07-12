from geckordp.actors.actor import Actor


class PreferenceActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/preference.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_traits(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getTraits",
        })

    def get_bool_pref(self, value):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getBoolPref",
            "value": value
        })

    def get_char_pref(self, value):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getCharPref",
            "value": value
        })

    def get_int_pref(self, value):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getIntPref",
            "value": value
        })

    def get_all_prefs(self, value):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getAllPrefs",
            "value": value
        }, "value")

    def set_bool_pref(self, name: str, value):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "setBoolPref",
            "name": name,
            "value": value,
        })

    def set_char_pref(self, name: str, value):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "setCharPref",
            "name": name,
            "value": value,
        })

    def set_int_pref(self, name: str, value):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "setIntPref",
            "name": name,
            "value": value,
        })

    def clear_user_pref(self, name: str):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "clearUserPref",
            "name": name,
        })
