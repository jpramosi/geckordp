from typing import List
from geckordp.actors.actor import Actor


class NetworkParentActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/network-parent.js
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_persist(self, enabled: bool):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "setPersist",
            "options": enabled,
        })

    def set_network_throttling(self, download_throughput: int, upload_throughput: int, latency_ms: int):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "setNetworkThrottling",
            "options": {
                "downloadThroughput": download_throughput,
                "uploadThroughput": upload_throughput,
                "latency": latency_ms
            },
        })

    def get_network_throttling(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getNetworkThrottling",
        })

    def clear_network_throttling(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "clearNetworkThrottling",
        })

    def set_save_request_and_response_bodies(self, save: bool):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "setSaveRequestAndResponseBodies",
            "save": save,
        })

    def set_blocked_urls(self, urls: List[str]):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "setBlockedUrls",
            "urls": urls,
        })

    def get_blocked_urls(self):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getBlockedUrls",
        })

    def block_request(self, filters: dict):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "blockRequest",
            "filters": filters,
        })

    def unblock_request(self, filters: dict):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "unblockRequest",
            "filters": filters,
        })
