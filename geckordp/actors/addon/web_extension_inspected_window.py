from geckordp.actors.actor import Actor


class WebExtensionInspectedWindowActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/addon/webextension-inspected-window.js
        https://github.com/mozilla/gecko-dev/blob/master/devtools/server/actors/addon/webextension-inspected-window.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def reload(self, url: str, line: int, addon_id: str, ignore_cache=False, user_agent="", injected_script=""):
        response = self.client.request_response({
            "to": self.actor_id,
            "type": "reload",
            "webExtensionCallerInfo": {
                "url": url,
                "lineNumber": line,
                "addonId": addon_id,
            },
            "options": {
                "ignoreCache": ignore_cache,
                "userAgent": user_agent,
                "injectedScript": injected_script,
            }
        })
        return response.get("walker", response)

    def eval(self, expression: str, url: str, line: int, addon_id: str):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "eval",
            "webExtensionCallerInfo": {
                "url": url,
                "lineNumber": line,
                "addonId": addon_id,
            },
            "expression": expression,
        })

    # options not supported yet
    """def eval(self, expression: str, url: str, line: int, addon_id: str,
             use_content_script_context=True, frame_url="",
             context_security_origin="", eval_result_as_grip=False,
             toolbox_selected_node_actor_id="", toolbox_console_actor_id=""):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "eval",
            "webExtensionCallerInfo": {
                "url": url,
                "lineNumber": line,
                "addonId": addon_id,
            },
            "expression": expression,
            "options": {
                "frameURL": frame_url,
                "contextSecurityOrigin": context_security_origin,
                "useContentScriptContext": use_content_script_context,
                "evalResultAsGrip": eval_result_as_grip,
                "toolboxSelectedNodeActorID": toolbox_selected_node_actor_id,
                "toolboxConsoleActorID": toolbox_console_actor_id,
            }
        })
     """
