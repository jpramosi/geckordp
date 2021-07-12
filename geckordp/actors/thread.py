from enum import Enum
from geckordp.actors.actor import Actor


class ThreadActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/thread.js
    """

    class ResumeLimit(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/7ef5cefd0468b8f509efe38e0212de2398f4c8b3/devtools/client/fronts/thread.js#L129
        """
        NONE = None
        BREAK = "break"
        NEXT = "next"
        STEP = "step"
        FINISH = "finish"
        RESTART = "restart"

    class When(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/f1451cbda60df2f90ed2d5637dcc38615019a07c/devtools/server/actors/thread.js#L1579
        """
        NOW = ""
        ON_NEXT = "onNext"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def attach(self,
               pause_on_exceptions=False,
               ignore_caught_exceptions=True,
               should_show_overlay=False,
               should_include_saved_frames=True,
               should_include_async_live_frames=False,
               skip_breakpoints=False,
               log_event_breakpoints=False,
               observe_asm_js=True,
               breakpoints=None,
               event_breakpoints=None):
        if (breakpoints == None):
            breakpoints = {}
        if (event_breakpoints == None):
            event_breakpoints = []
        return self.client.request_response({
            "to": self.actor_id,
            "type": "attach",
            "options": {
                "pauseOnExceptions": pause_on_exceptions,
                "ignoreCaughtExceptions": ignore_caught_exceptions,
                "shouldShowOverlay": should_show_overlay,
                "shouldIncludeSavedFrames": should_include_saved_frames,
                "shouldIncludeAsyncLiveFrames": should_include_async_live_frames,
                "skipBreakpoints": skip_breakpoints,
                "logEventBreakpoints": log_event_breakpoints,
                "observeAsmJS": observe_asm_js,
                "breakpoints": breakpoints,
                "eventBreakpoints": event_breakpoints,
            },
        })

    def reconfigure(self,
                    observe_asm_js=True,
                    pause_workers_until_attach=True,
                    skip_breakpoints=None,
                    log_event_breakpoints=None):
        if (skip_breakpoints == None):
            skip_breakpoints = {}
        if (log_event_breakpoints == None):
            log_event_breakpoints = []
        return self.client.request_response({
            "to": self.actor_id,
            "type": "reconfigure",
            "options": {
                "observeAsmJS": observe_asm_js,
                "pauseWorkersUntilAttach": pause_workers_until_attach,
                "skipBreakpoints": skip_breakpoints,
                "logEventBreakpoints": log_event_breakpoints,
            },
        })

    def resume(self, resume_limit=ResumeLimit.NONE, frame_actor_id=""):
        args = {
            "to": self.actor_id,
            "type": "resume",
        }
        if (resume_limit == ThreadActor.ResumeLimit.NONE):
            args["resumeLimit"] = None
        else:
            args["resumeLimit"] = resume_limit.value
        if (frame_actor_id != ""):
            args["frameActorID"] = frame_actor_id
        return self.client.request_response(args)

    def frames(self, start: int, count: int):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "frames",
            "start": start,
            "count": count,
        }, "frames")

    def interrupt(self, when=When.NOW):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "interrupt",
            "when": when.value,
        })

    def sources(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "sources",
        }, "sources")

    def skip_breakpoints(self, skip_breakpoints=None):
        if (skip_breakpoints == None):
            skip_breakpoints = {}
        # todo couldn't find any correct usage
        return self.client.request_response({
            "to": self.actor_id,
            "type": "skipBreakpoints",
            "skip": skip_breakpoints,
        })

    def dump_thread(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "dumpThread",
        })

    def dump_pools(self):
        # todo response doesn't follow the usual structure
        # and won't work with rdpclient, maybe
        # firefox devs will change this in the future
        return self.client.request_response({
            "to": self.actor_id,
            "type": "dumpPools",
        })

    def set_breakpoint(self,
                       line: int,
                       column: int,
                       source_url="",
                       source_id="",
                       condition="",
                       log_value=""):
        """ https://github.com/mozilla/gecko-dev/blob/f1451cbda60df2f90ed2d5637dcc38615019a07c/devtools/server/actors/thread.js#L568
        """
        args = {
            "to": self.actor_id,
            "type": "setBreakpoint",
            "location": {
                "line": line,
                "column": column,
            },
            "options": {}
        }
        if (source_url != ""):
            args["location"]["sourceUrl"] = source_url
        if (source_id != ""):
            args["location"]["sourceId"] = source_id
        if (condition != ""):
            args["options"]["condition"] = condition
        if (log_value != ""):
            args["options"]["logValue"] = log_value
        return self.client.request_response(args)

    def remove_breakpoint(self,
                          line: int,
                          column: int,
                          source_url="",
                          source_id=""):
        args = {
            "to": self.actor_id,
            "type": "removeBreakpoint",
            "location": {
                "line": line,
                "column": column,
            }
        }
        if (source_url != ""):
            args["location"]["sourceUrl"] = source_url
        if (source_id != ""):
            args["location"]["sourceId"] = source_id
        return self.client.request_response(args)

    def set_xhr_breakpoint(self, path: str, method="ANY"):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "setXHRBreakpoint",
            "path": path,
            "method": method,
        }, "value")

    def remove_xhr_breakpoint(self, path: str, method: str):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "removeXHRBreakpoint",
            "path": path,
            "method": method,
        }, "value")

    def get_available_event_breakpoints(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getAvailableEventBreakpoints",
        }, "value")

    def get_active_event_breakpoints(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getActiveEventBreakpoints",
        }, "ids")

    def set_active_event_breakpoints(self, ids: list):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "setActiveEventBreakpoints",
            "ids": ids,
        })

    def pause_on_exceptions(self, pause_on_exceptions: str, ignore_caught_exceptions: str):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "pauseOnExceptions",
            "pauseOnExceptions": pause_on_exceptions,
            "ignoreCaughtExceptions": ignore_caught_exceptions,
        })

    def toggle_event_logging(self, log_event_breakpoints: str):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "toggleEventLogging",
            "logEventBreakpoints": log_event_breakpoints,
        })

    def is_attached(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "isAttached",
        }, "value")
