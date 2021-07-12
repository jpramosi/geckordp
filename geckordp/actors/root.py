from geckordp.actors.actor import Actor


class RootActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/root.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actor_id = "root"

    def get_root(self):
        return self.client.request_response({
            "to": "root",
            "type": "getRoot"
        })

    def list_tabs(self):
        return self.client.request_response({
            "to": "root",
            "type": "listTabs"
        }, "tabs")

    def get_tab(self, outer_window_id : int):
        return self.client.request_response({
            "to": "root",
            "type": "getTab",
            "outerWindowID": outer_window_id,
        })

    def list_addons(self):
        return self.client.request_response({
            "to": "root",
            "type": "listAddons"
        }, "addons")

    def list_workers(self):
        return self.client.request_response({
            "to": "root",
            "type": "listWorkers"
        }, "workers")

    def list_service_worker_registrations(self):
        return self.client.request_response({
            "to": "root",
            "type": "listServiceWorkerRegistrations"
        }, "registrations")

    def list_processes(self):
        return self.client.request_response({
            "to": "root",
            "type": "listProcesses"
        }, "processes")

    def get_process(self, pid : int):
        return self.client.request_response({
            "to": "root",
            "type": "getProcess",
            "id": pid,
        })

    def request_types(self):
        return self.client.request_response({
            "to": "root",
            "type": "requestTypes"
        }, "requestTypes")

    def echo(self, text : str):
        return self.client.request_response({
            "to": "root",
            "type": "echo",
            "text": f"{text}",
        })

    def current_tab(self):
        return self.client.request_response({
            "to": "root",
            "type": "listTabs"
        }, "tabs[?selected==`true`] | [0]")
