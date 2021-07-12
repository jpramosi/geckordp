from enum import Enum
from geckordp.actors.actor import Actor


class WalkerActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/walker.js

        .. warning:: Expiremental actor! Currently no tests but roughly tested.
    """

    class Position(str, Enum):
        """ https://developer.mozilla.org/en-US/docs/Web/API/Element/insertAdjacentHTML#parameters
        """
        BEFORE_BEGIN = "beforeBegin"
        AFTER_BEGIN = "afterBegin"
        BEFORE_END = "beforeEnd"
        AFTER_END = "afterEnd"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def release(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "release",
        })

    def document(self, dom_node_actor=""):
        response = self.client.request_response({
            "to": self.actor_id,
            "type": "document",
            "node": dom_node_actor,
        })
        return response.get("node", response)

    def document_element(self, dom_node_actor: str):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "documentElement",
            "node": dom_node_actor,
        })

    def retain_node(self, dom_node_actor: str):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "retainNode",
            "node": dom_node_actor,
        })

    def unretain_node(self, dom_node_actor: str):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "unretainNode",
            "node": dom_node_actor,
        })

    def release_node(self, dom_node_actor: str):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "releaseNode",
            "node": dom_node_actor,
        })

    def children(self, dom_node_actor: str, max_nodes=1000, center_node="", start_node="", what_to_show=""):
        response = self.client.request_response({
            "to": self.actor_id,
            "type": "children",
            "node": dom_node_actor,
            "maxNodes": max_nodes,
            "center": center_node,
            "start": start_node,
            "whatToShow": what_to_show,
        })
        return response.get("nodes", response)

    def next_sibling(self, dom_node_actor: str, what_to_show=""):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "nextSibling",
            "node": dom_node_actor,
            "whatToShow": what_to_show,
        })

    def previous_sibling(self, dom_node_actor: str, what_to_show=""):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "previousSibling",
            "node": dom_node_actor,
            "whatToShow": what_to_show,
        })

    def find_inspecting_node(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "findInspectingNode",
        })

    def query_selector(self, dom_node_actor: str, selector):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "querySelector",
            "node": dom_node_actor,
            "selector": selector,
        })

    def query_selector_all(self, dom_node_actor: str, selector):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "querySelectorAll",
            "node": dom_node_actor,
            "selector": selector,
        })

    def multi_frame_query_selector_all(self, selector):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "multiFrameQuerySelectorAll",
            "selector": selector,
        })

    def search(self, query):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "search",
            "query": query,
        })

    def get_suggestions_for_query(self, query, completing, selector_state):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getSuggestionsForQuery",
            "query": query,
            "completing": completing,
            "selectorState": selector_state,
        })

    def add_pseudo_class_lock(self, dom_node_actor: str, pseudo_class, parents, enabled: bool):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "addPseudoClassLock",
            "node": dom_node_actor,
            "pseudoClass": pseudo_class,
            "parents": parents,
            "enabled": enabled,
        })

    def hide_node(self, dom_node_actor: str):
        return self.client.request({
            "to": self.actor_id,
            "type": "hideNode",
            "node": dom_node_actor,
        })

    def unhide_node(self, dom_node_actor: str):
        return self.client.request({
            "to": self.actor_id,
            "type": "unhideNode",
            "node": dom_node_actor,
        })

    def remove_pseudo_class_lock(self, dom_node_actor: str, pseudo_class, parents):
        return self.client.request({
            "to": self.actor_id,
            "type": "removePseudoClassLock",
            "node": dom_node_actor,
            "pseudoClass": pseudo_class,
            "parents": parents,
        })

    def clear_pseudo_class_locks(self, dom_node_actor: str):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "clearPseudoClassLocks",
            "node": dom_node_actor,
        })

    def inner_html(self, dom_node_actor: str):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "innerHTML",
            "node": dom_node_actor,
        })

    def set_inner_html(self, dom_node_actor: str, value: str):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "setInnerHTML",
            "node": dom_node_actor,
            "value": value,
        })

    def outer_html(self, dom_node_actor: str):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "outerHTML",
            "node": dom_node_actor,
        })

    def set_outer_html(self, dom_node_actor: str, value: str):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "setOuterHTML",
            "node": dom_node_actor,
            "value": value,
        })

    def insert_adjacent_html(self, dom_node_actor: str, position: Position, value: str):
        """ see https://developer.mozilla.org/en-US/docs/Web/API/Element/insertAdjacentHTML
        """
        return self.client.request_response({
            "to": self.actor_id,
            "type": "insertAdjacentHTML",
            "node": dom_node_actor,
            "position": position.value,
            "value": value,
        })

    def duplicate_node(self, dom_node_actor: str):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "duplicateNode",
            "node": dom_node_actor,
        })

    def remove_node(self, dom_node_actor: str):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "removeNode",
            "node": dom_node_actor,
        })

    def remove_nodes(self, dom_node_actors: []):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "removeNode",
            "node": dom_node_actors,
        })

    def insert_before(self, dom_node_actor: str, parent_node: str, sibling_node=""):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "insertBefore",
            "node": dom_node_actor,
            "parent": parent_node,
            "sibling": sibling_node,
        })

    def edit_tag_name(self, dom_node_actor: str, tag_name: str):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "editTagName",
            "node": dom_node_actor,
            "tagName": tag_name,
        })

    def get_mutations(self, cleanup: bool):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getMutations",
            "cleanup": cleanup,
        })

    def is_in_dom_tree(self, dom_node_actor: str):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "isInDOMTree",
            "node": dom_node_actor,
        })

    def get_node_actor_from_window_id(self, window_id: str):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getNodeActorFromWindowID",
            "windowID": window_id,
        })

    def get_node_actor_from_content_dom_reference(self, content_dom_ref):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getNodeActorFromContentDomReference",
            "contentDomReference": content_dom_ref,
        })

    def get_style_sheet_owner_node(self, style_sheet_actor_id: str):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getStyleSheetOwnerNode",
            "styleSheetActorID": style_sheet_actor_id,
        })

    def get_node_from_actor(self, actor_id: str, paths: []):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getNodeFromActor",
            "actorID": actor_id,
            "path": paths,
        })

    def get_layout_inspector(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getLayoutInspector",
        })

    def get_parent_grid_node(self, dom_node_actor=""):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getParentGridNode",
            "node": dom_node_actor,
        })

    def get_offset_parent(self, dom_node_actor=""):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getOffsetParent",
            "node": dom_node_actor,
        })

    def set_mutation_breakpoints(self, dom_node_actor: str, subtree: bool, removal: bool, attribute: bool):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "setMutationBreakpoints",
            "node": dom_node_actor,
            "subtree": subtree,
            "removal": removal,
            "attribute": attribute,
        })

    def get_embedder_element(self, browsing_context_id: str):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getEmbedderElement",
            "browsingContextID": browsing_context_id,
        })

    def pick(self, focus: bool):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "pick",
            "doFocus": focus,
        })

    def cancel_pick(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "cancelPick",
        })

    def watch_root_node(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "watchRootNode",
        })

    def get_overflow_causing_elements(self, dom_node_actor: str):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getOverflowCausingElements",
            "node": dom_node_actor,
        })

    def get_scrollable_ancestor_node(self, dom_node_actor: str):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getScrollableAncestorNode",
            "node": dom_node_actor,
        })
