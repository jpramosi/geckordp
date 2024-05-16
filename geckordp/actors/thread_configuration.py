from geckordp.actors.actor import Actor


class ThreadConfigurationActor(Actor):
    """https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/thread-configuration.js"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_configuration(
        self,
        should_pause_on_debugger_statement: bool | None = None,
        pause_on_exceptions: bool | None = None,
        ignore_caught_exceptions: bool | None = None,
        should_include_saved_frames: bool | None = None,
        should_include_async_live_frames: bool | None = None,
        skip_breakpoints: bool | None = None,
        log_event_breakpoints: bool | None = None,
        observe_asm_js: bool | None = None,
        pause_overlay: bool | None = None,
    ):
        args = {}

        if should_pause_on_debugger_statement is not None:
            args["shouldPauseOnDebuggerStatement"] = should_pause_on_debugger_statement

        if pause_on_exceptions is not None:
            args["pauseOnExceptions"] = pause_on_exceptions

        if ignore_caught_exceptions is not None:
            args["ignoreCaughtExceptions"] = ignore_caught_exceptions

        if should_include_saved_frames is not None:
            args["shouldIncludeSavedFrames"] = should_include_saved_frames

        if should_include_async_live_frames is not None:
            args["shouldIncludeAsyncLiveFrames"] = should_include_async_live_frames

        if skip_breakpoints is not None:
            args["skipBreakpoints"] = skip_breakpoints

        if log_event_breakpoints is not None:
            args["logEventBreakpoints"] = log_event_breakpoints

        if observe_asm_js is not None:
            args["observeAsmJS"] = observe_asm_js

        if pause_overlay is not None:
            args["pauseOverlay"] = pause_overlay

        return self.client.send_receive(
            {
                "to": self.actor_id,
                "type": "updateConfiguration",
                "configuration": args,
            }
        )
