from geckordp.actors.actor import Actor


class AccessibleWalkerActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/accessibility.js#L130
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def children(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "children",
        }, "children")

    def get_accessible_for(self, dom_node_actor: str):
        # 'dom_node_actor' can be retrieved from WalkerActor
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getAccessibleFor",
            "node": dom_node_actor,
        })

    def get_ancestry(self, accessible):
        # probably needs the accesible object from 'get_accessible_for()'
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getAncestry",
            "accessible": accessible,
        }, "ancestry")

    def start_audit(self, options: dict = None):
        if (options is None):
            options = {}
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "startAudit",
            "options": options,
        })

    def highlight_accessible(self, accessible,  options: dict = None):
        # probably needs the accesible object from 'get_accessible_for()'
        if (options is None):
            options = {}
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "highlightAccessible",
            "accessible": accessible,
            "options": options,
        })

    def unhighlight(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "unhighlight",
        })

    def cancel_pick(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "cancelPick",
        })

    def pick_and_focus(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "pickAndFocus",
        })

    def show_tabbing_order(self, dom_node_actor: str, index: int):
        # 'dom_node_actor' can be retrieved from WalkerActor
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "showTabbingOrder",
            "elm": dom_node_actor,
            "index": index,
        })
