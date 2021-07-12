from geckordp.actors.actor import Actor


class NetworkEventActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/network-event.js
        https://github.com/mozilla/gecko-dev/blob/7ef5cefd0468b8f509efe38e0212de2398f4c8b3/devtools/client/netmonitor/src/actions/search.js#L105
        https://github.com/mozilla/gecko-dev/blob/7ef5cefd0468b8f509efe38e0212de2398f4c8b3/devtools/client/netmonitor/src/constants.js#L153

        .. note:: The 'actor_id' a.k.a. 'netEvent' must be taken from ["type": "resource-available-form"] event and not ["type": "networkEvent"].
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def release(self):
        """ If data is not needed anymore, it can be freed on the serverside.
            Following calls to other functions after 'release()' will fail.
        """
        return self.client.request_response({
            "to": self.actor_id,
            "type": "release",
        })

    def get_request_headers(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getRequestHeaders",
        })

    def get_request_cookies(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getRequestCookies",
        })

    def get_request_post_data(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getRequestPostData",
        })

    def get_response_headers(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getResponseHeaders",
        })

    def get_response_cookies(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getResponseCookies",
        })

    def get_response_cache(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getResponseCache",
        })

    def get_response_content(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getResponseContent",
        })

    def get_event_timings(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getEventTimings",
        })

    def get_security_info(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getSecurityInfo",
        })

    # todo: "Spec for 'netEvent' specifies a 'getStackTrace' method that isn't implemented by the actor",
    """ def get_stack_trace(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getStackTrace",
        }) """
