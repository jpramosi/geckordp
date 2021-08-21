from geckordp.actors.actor import Actor


class TargetConfigurationActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/target-configuration.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_configuration(self,
                             cache_disabled: bool = None,
                             color_scheme_simulation: bool = None,
                             custom_user_agent="",
                             javascript_enabled: bool = None,
                             override_dppx=-1,
                             paint_flashing: bool = None,
                             print_simulation_enabled: bool = None,
                             restore_focus: bool = None,
                             service_workers_testing_enabled: bool = None,
                             touch_events_override=""):
        args = {}

        if (cache_disabled is not None):
            args["cacheDisabled"] = cache_disabled

        if (color_scheme_simulation is not None):
            args["colorSchemeSimulation"] = color_scheme_simulation

        if (custom_user_agent != ""):
            args["customUserAgent"] = custom_user_agent

        if (javascript_enabled is not None):
            args["javascriptEnabled"] = javascript_enabled

        if (override_dppx != -1):
            args["overrideDPPX"] = override_dppx

        if (paint_flashing is not None):
            args["paintFlashing"] = paint_flashing

        if (print_simulation_enabled is not None):
            args["printSimulationEnabled"] = print_simulation_enabled

        if (restore_focus is not None):
            args["restoreFocus"] = restore_focus

        if (service_workers_testing_enabled is not None):
            args["serviceWorkersTestingEnabled"] = service_workers_testing_enabled

        if (touch_events_override != ""):
            args["touchEventsOverride"] = touch_events_override

        return self.client.send_receive({
            "to": self.actor_id,
            "type": "updateConfiguration",
            "configuration": args,
        })
