from enum import Enum
from geckordp.actors.actor import Actor


class InspectorActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/inspector.js
    """

    class Highlighters(str, Enum):
        """ https://firefox-source-docs.mozilla.org/devtools/tools/highlighters.html#using-highlighters
        """
        CSS_GRID_HIGHLIGHTER = "CssGridHighlighter"
        BOX_MODEL_HIGHLIGHTER = "BoxModelHighlighter"
        CSS_TRANSFORM_HIGHLIGHTER = "CssTransformHighlighter"
        FLEXBOX_HIGHLIGHTER = "FlexboxHighlighter"
        FONTS_HIGHLIGHTER = "FontsHighlighter"
        GEOMETRY_EDITOR_HIGHLIGHTER = "GeometryEditorHighlighter"
        MEASURING_TOOL_HIGHLIGHTER = "MeasuringToolHighlighter"
        PAUSED_DEBUGGER_OVERLAY = "PausedDebuggerOverlay"
        RULERS_HIGHLIGHTER = "RulersHighlighter"
        SELECTOR_HIGHLIGHTER = "SelectorHighlighter"
        SHAPES_HIGHLIGHTER = "ShapesHighlighter"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_walker(self, options_json=None):
        if (options_json is None):
            options_json = {}
        response = self.client.send_receive({
            "to": self.actor_id,
            "type": "getWalker",
            "options": options_json,
        })
        return response.get("walker", response)

    def get_page_style(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getPageStyle",
        })

    def get_compatibility(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getCompatibility",
        })

    def get_highlighter_by_type(self, hightligher_type: Highlighters):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getHighlighterByType",
            "typeName": hightligher_type.value,
        })

    def get_image_data_from_url(self, url: str, max_dim=0):
        args = {
            "to": self.actor_id,
            "type": "getImageDataFromURL",
            "url": url,
        }
        if (max_dim > 0):
            args["maxDim"] = max_dim
        return self.client.send_receive(args)

    def resolve_relative_url(self, url: str, dom_node_actor: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "resolveRelativeURL",
            "url": url,
            "node": dom_node_actor,
        })

    def pick_color_from_page(self, options_json: dict):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "pickColorFromPage",
            "options": options_json,
        })

    def cancel_pick_color_from_page(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "cancelPickColorFromPage",
        })

    def supports_highlighters(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "supportsHighlighters",
        })
