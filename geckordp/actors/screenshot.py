from geckordp.actors.actor import Actor


class ScreenshotActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/screenshot.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def capture(self,
                browsing_context_id: int,
                fullpage=True,
                file=False,
                copy_clipboard=False,
                selector="",
                dpr=2,
                delay_sec=0,
                snapshot_scale=1,
                left=None,
                top=None,
                width=None,
                height=None):
        args = {
            "fullpage": fullpage,
            "file": file,
            "clipboard": copy_clipboard,
            "selector": selector,
            "dpr": str(dpr),
            "delay": str(delay_sec),
            "snapshotScale": snapshot_scale,
            "browsingContextID": browsing_context_id,
        }
        if (left and top and width and height):
            args["rect"] = {
                "left": left,
                "top": top,
                "width": width,
                "height": height
            }
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "capture",
            "args": args,
        })
