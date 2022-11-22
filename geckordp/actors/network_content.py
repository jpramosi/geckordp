from geckordp.actors.actor import Actor


class NetworkContentActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/network-content.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def send_http_request(self,
                          url: str,
                          method="GET",
                          headers: dict | None = None,
                          body=""):
        if (headers is None):
            """
            {
                "Host": "www.duckduckgo.com",
                "User-Agent": "my-user-agent",
            }
            """
            headers = {}
        nheaders = []
        for name, value in headers.items():
            nheaders.append({
                "name": name,
                "value": value,
            })
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "sendHTTPRequest",
            "request": {
                "cause": {
                    "type": "document",
                    "loadingDocumentUri": None,
                    "stacktraceAvailable": True,
                    "lastFrame": {},
                },
                "url": url,
                "method": method.upper(),
                "headers": nheaders,
                "body": body,
            },
        })

    def get_stack_trace(self, resource_id: int):
        # todo: on firefox-100.0 'get_stack_trace()' doesn't seem to work anymore,
        # even if 'WatcherActor.watch_resources()' was successful
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getStackTrace",
            "resourceId": resource_id,
        })
