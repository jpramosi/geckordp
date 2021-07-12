from geckordp.actors.actor import Actor


class SourceActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/source.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_breakpoint_positions(self,
                                 start_line=0,
                                 start_column=0,
                                 end_line=10**10,
                                 end_column=10**10):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getBreakpointPositions",
            "query": {
                "start": {
                    "line": start_line,
                    "column": start_column,
                },
                "end": {
                    "line": end_line,
                    "column": end_column,
                },
            }
        }, "positions")

    def get_breakpoint_positions_compressed(self,
                                            start_line=0,
                                            start_column=0,
                                            end_line=10**10,
                                            end_column=10**10):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getBreakpointPositionsCompressed",
            "query": {
                "start": {
                    "line": start_line,
                    "column": start_column,
                },
                "end": {
                    "line": end_line,
                    "column": end_column,
                },
            }
        })

    def get_breakable_lines(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getBreakableLines",
        })

    def source(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "source",
        })

    def set_pause_point(self,
                        line: int,
                        column: int,
                        breakpoint_=True,
                        stepover=True):
        # https://github.com/mozilla/gecko-dev/blob/7ef5cefd0468b8f509efe38e0212de2398f4c8b3/devtools/server/tests/xpcshell/test_stepping-with-skip-breakpoints.js#L34
        return self.client.request_response({
            "to": self.actor_id,
            "type": "setPausePoints",
            "pausePoints": [
                {
                    "location": {
                        "line": line,
                        "column": column,
                    },
                    "types": {
                        "breakpoint": breakpoint_,
                        "stepOver": stepover,
                    },
                },
            ],
        })

    def set_pause_points(self, pause_points=None):
        # https://github.com/mozilla/gecko-dev/blob/7ef5cefd0468b8f509efe38e0212de2398f4c8b3/devtools/server/tests/xpcshell/test_stepping-with-skip-breakpoints.js#L34
        if (pause_points == None):
            pause_points = [
                # point 1
                {
                    "location": {
                        "line": 0,
                        "column": 0,
                    },
                    "types": {
                        "breakpoint": True,
                        "stepOver": True,
                    },
                },
                # point 2
                {
                    "location": {
                        "line": 1,
                        "column": 0,
                    },
                    "types": {
                        "breakpoint": True,
                        "stepOver": True,
                    },
                },
            ]
        return self.client.request_response({
            "to": self.actor_id,
            "type": "setPausePoints",
            "pausePoints": pause_points,
        })

    def blackbox(self,
                 start_line: int,
                 start_column: int,
                 end_line: int,
                 end_column: int):
        # https://github.com/mozilla/gecko-dev/blob/7ef5cefd0468b8f509efe38e0212de2398f4c8b3/devtools/server/tests/xpcshell/test_blackboxing-03.js#L62
        return self.client.request_response({
            "to": self.actor_id,
            "type": "blackbox",
            "range": {
                "start": {
                    "line": start_line,
                    "column": start_column,
                },
                "end": {
                    "line": end_line,
                    "column": end_column,
                },
            },
        })

    def unblackbox(self,
                   start_line: int,
                   start_column: int,
                   end_line: int,
                   end_column: int):
        # https://github.com/mozilla/gecko-dev/blob/7ef5cefd0468b8f509efe38e0212de2398f4c8b3/devtools/server/tests/xpcshell/test_blackboxing-03.js#L62
        return self.client.request_response({
            "to": self.actor_id,
            "type": "unblackbox",
            "ranges": {
                "start": {
                    "line": start_line,
                    "column": start_column,
                },
                "end": {
                    "line": end_line,
                    "column": end_column,
                },
            },
        })
