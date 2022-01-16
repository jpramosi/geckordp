from geckordp.actors.actor import Actor


class NodeActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/node.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_node_value(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getNodeValue",
        }, "value")

    def set_node_value(self, value):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "setNodeValue",
            "value": value,
        })

    def get_unique_selector(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getUniqueSelector",
        }, "value")

    def get_css_path(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getCssPath",
        }, "value")

    def get_x_path(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getXPath",
        }, "value")

    def scroll_into_view(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "scrollIntoView",
        })

    def get_image_data(self, max_dim=0):
        args = {
            "to": self.actor_id,
            "type": "getImageData",
        }
        if (max_dim > 0):
            args["maxDim"] = max_dim
        return self.client.send_receive(args)

    def get_event_listener_info(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getEventListenerInfo",
        }, "events")

    def modify_attributes(self, modifications: list):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "modifyAttributes",
            "modifications": modifications,
        })

    def get_font_family_data_url(self, font: str, fill_style=""):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getFontFamilyDataURL",
            "font": font,
            "fillStyle": fill_style,
        })

    def get_closest_background_color(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getClosestBackgroundColor",
        }, "value")

    def get_background_color(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getBackgroundColor",
        }, "value")

    def get_owner_global_dimensions(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getOwnerGlobalDimensions",
        })

    """ def connect_to_remote_frame(self):
        # "Spec for 'domnode' specifies a 'connectToRemoteFrame' method that isn't implemented by the actor"
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "connectToRemoteFrame",
        }) """

    def wait_for_frame_load(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "waitForFrameLoad",
        })
