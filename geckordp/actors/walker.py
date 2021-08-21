from enum import Enum
from typing import List
from geckordp.actors.actor import Actor


class WalkerActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/walker.js
    """

    class Position(str, Enum):
        """ https://developer.mozilla.org/en-US/docs/Web/API/Element/insertAdjacentHTML#parameters
        """
        BEFORE_BEGIN = "beforeBegin"
        AFTER_BEGIN = "afterBegin"
        BEFORE_END = "beforeEnd"
        AFTER_END = "afterEnd"

    class PseudoClass(str, Enum):
        """ https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Examine_and_edit_CSS#viewing_common_pseudo-classes
        """
        HOVER = ":hover"
        ACTIVE = ":active"
        FOCUS = ":focus"
        FOCUS_VISIBLE = ":focus-visible"
        FOCUS_WITHIN = ":focus-within"
        VISITED = ":visited"
        TARGET = ":target"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def release(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "release",
        })

    def document(self, dom_node_actor=""):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "document",
            "node": dom_node_actor,
        }, "node")

    def document_element(self, dom_node_actor: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "documentElement",
            "node": dom_node_actor,
        }, "node")

    def retain_node(self, dom_node_actor: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "retainNode",
            "node": dom_node_actor,
        })

    def unretain_node(self, dom_node_actor: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "unretainNode",
            "node": dom_node_actor,
        })

    def release_node(self, dom_node_actor: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "releaseNode",
            "node": dom_node_actor,
        })

    def children(self, dom_node_actor: str, max_nodes=1000, center_node="", start_node="", what_to_show=""):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "children",
            "node": dom_node_actor,
            "maxNodes": max_nodes,
            "center": center_node,
            "start": start_node,
            "whatToShow": what_to_show,
        }, "nodes")

    def next_sibling(self, dom_node_actor: str, what_to_show=""):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "nextSibling",
            "node": dom_node_actor,
            "whatToShow": what_to_show,
        }, "node")

    def previous_sibling(self, dom_node_actor: str, what_to_show=""):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "previousSibling",
            "node": dom_node_actor,
            "whatToShow": what_to_show,
        }, "node")

    def find_inspecting_node(self):
        # "Spec for 'domwalker' specifies a 'findInspectingNode' method that isn't implemented by the actor"
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "findInspectingNode",
        })

    def query_selector(self, dom_node_actor: str, selector: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "querySelector",
            "node": dom_node_actor,
            "selector": selector,
        })

    def query_selector_all(self, dom_node_actor: str, selector: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "querySelectorAll",
            "node": dom_node_actor,
            "selector": selector,
        }, "list")

    def multi_frame_query_selector_all(self, selector: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "multiFrameQuerySelectorAll",
            "selector": selector,
        }, "list")

    def search(self, query):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "search",
            "query": query,
        }, "list")

    def get_suggestions_for_query(self, completing: str, query="", selector_state="tag"):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getSuggestionsForQuery",
            "query": query,
            "completing": completing,
            "selectorState": selector_state,
        })

    def add_pseudo_class_lock(self, dom_node_actor: str, pseudo_class: PseudoClass, parents: bool):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "addPseudoClassLock",
            "node": dom_node_actor,
            "pseudoClass": pseudo_class.value,
            "parents": parents,
        })

    def hide_node(self, dom_node_actor: str):
        # "node.rawNode.classList is undefined"
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "hideNode",
            "node": dom_node_actor,
        })

    def unhide_node(self, dom_node_actor: str):
        # "node.rawNode.classList is undefined"
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "unhideNode",
            "node": dom_node_actor,
        })

    def remove_pseudo_class_lock(self, dom_node_actor: str, pseudo_class: PseudoClass, parents: bool):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "removePseudoClassLock",
            "node": dom_node_actor,
            "pseudoClass": pseudo_class.value,
            "parents": parents,
        })

    def clear_pseudo_class_locks(self, dom_node_actor: str):
        # "InspectorUtils.clearPseudoClassLocks: Argument 1 does not implement interface Element."
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "clearPseudoClassLocks",
            "node": dom_node_actor,
        })

    def inner_html(self, dom_node_actor: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "innerHTML",
            "node": dom_node_actor,
        }, "value")

    def set_inner_html(self, dom_node_actor: str, value: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "setInnerHTML",
            "node": dom_node_actor,
            "value": value,
        })

    def outer_html(self, dom_node_actor: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "outerHTML",
            "node": dom_node_actor,
        }, "value")

    def set_outer_html(self, dom_node_actor: str, value: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "setOuterHTML",
            "node": dom_node_actor,
            "value": value,
        })

    def insert_adjacent_html(self, dom_node_actor: str, position: Position, value: str):
        """ see https://developer.mozilla.org/en-US/docs/Web/API/Element/insertAdjacentHTML
        """
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "insertAdjacentHTML",
            "node": dom_node_actor,
            "position": position.value,
            "value": value,
        })

    def duplicate_node(self, dom_node_actor: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "duplicateNode",
            "node": dom_node_actor,
        })

    def remove_node(self, dom_node_actor: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "removeNode",
            "node": dom_node_actor,
        })

    def remove_nodes(self, dom_node_actors: List[str]):
        # "Cannot remove document, document elements or dead nodes."
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "removeNode",
            "node": dom_node_actors,
        })

    def insert_before(self, dom_node_actor: str, parent_dom_node_actor: str, sibling_dom_node_actor=""):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "insertBefore",
            "node": dom_node_actor,
            "parent": parent_dom_node_actor,
            "sibling": sibling_dom_node_actor,
        })

    def edit_tag_name(self, dom_node_actor: str, tag_name: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "editTagName",
            "node": dom_node_actor,
            "tagName": tag_name,
        })

    def get_mutations(self, cleanup: bool):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getMutations",
            "cleanup": cleanup,
        }, "mutations")

    def is_in_dom_tree(self, dom_node_actor: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "isInDOMTree",
            "node": dom_node_actor,
        })

    def get_node_actor_from_window_id(self, window_id: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getNodeActorFromWindowID",
            "windowID": window_id,
        }, "nodeFront")

    def get_node_actor_from_content_dom_reference(self, content_dom_ref: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getNodeActorFromContentDomReference",
            "contentDomReference": content_dom_ref,
        }, "nodeFront")

    def get_style_sheet_owner_node(self, style_sheet_actor_id: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getStyleSheetOwnerNode",
            "styleSheetActorID": style_sheet_actor_id,
        }, "ownerNode")

    def get_node_from_actor(self, actor_id: str, paths: List[str] = None):
        if (paths is None):
            paths = []
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getNodeFromActor",
            "actorID": actor_id,
            "path": paths,
        }, "node")

    def get_layout_inspector(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getLayoutInspector",
        }, "actor")

    def get_parent_grid_node(self, dom_node_actor: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getParentGridNode",
            "node": dom_node_actor,
        }, "node")

    def get_offset_parent(self, dom_node_actor: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getOffsetParent",
            "node": dom_node_actor,
        }, "node")

    def set_mutation_breakpoints(self, dom_node_actor: str, subtree: bool, removal: bool, attribute: bool):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "setMutationBreakpoints",
            "node": dom_node_actor,
            "subtree": subtree,
            "removal": removal,
            "attribute": attribute,
        })

    def get_embedder_element(self, browsing_context_id: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getEmbedderElement",
            "browsingContextID": browsing_context_id,
        })

    def pick(self, focus: bool):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "pick",
            "doFocus": focus,
        })

    def cancel_pick(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "cancelPick",
        })

    def watch_root_node(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "watchRootNode",
        })

    def get_overflow_causing_elements(self, dom_node_actor: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getOverflowCausingElements",
            "node": dom_node_actor,
        }, "list")

    def get_scrollable_ancestor_node(self, dom_node_actor: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getScrollableAncestorNode",
            "node": dom_node_actor,
        }, "node")
