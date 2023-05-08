from typing import List
from geckordp.actors.actor import Actor


# pylint: disable=invalid-name
class _impl_storage(Actor):

    def get_store_objects(self, host: str, names: List[str] | None = None, options: dict | None = None):
        if (options is None):
            options = {}
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getStoreObjects",
            "host": host,
            "names": names,
            "options": options,
        })

    def get_fields(self, sub_type: str | None = None):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "getFields",
            "subType": sub_type,
        })


# pylint: disable=invalid-name
class _impl_remove_item(Actor):

    def remove_item(self, host: str, name: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "removeItem",
            "host": host,
            "name": name,
        })


# pylint: disable=invalid-name
class _impl_add_item(Actor):

    def add_item(self, guid: str, host: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "addItem",
            "guid": guid,
            "host": host,
        })


# pylint: disable=invalid-name
class _impl_edit_item(Actor):

    def edit_item(self, data: dict):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "editItem",
            "data": data,
        })


# pylint: disable=invalid-name
class _impl_remove_all__host(Actor):

    def remove_all(self, host: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "removeAll",
            "host": host,
        })


# pylint: disable=invalid-name
class _impl_remove_all__host_name(Actor):

    def remove_all(self, host: str, name: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "removeAll",
            "host": host,
            "name": name,
        })


class CookieStorageActor(_impl_storage, _impl_add_item, _impl_remove_item):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/storage.js
    """

    def edit_item(self, host: str, field: str, old_value, new_value, cookie_data: dict):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "editItem",
            "data": {
                "host": host,
                "key": "uniqueKey",
                "field": field,
                "oldValue": old_value,
                "newValue": new_value,
                "items": cookie_data,
            },
        })

    def remove_all(self, host: str, domain: str | None = None):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "removeAll",
            "host": host,
            "domain": domain,
        })

    def remove_all_session_cookies(self, host: str, domain: str | None = None):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "removeAllSessionCookies",
            "host": host,
            "domain": domain,
        })


class LocalStorageActor(_impl_storage, _impl_add_item, _impl_remove_item, _impl_edit_item, _impl_remove_all__host):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/storage.js
    """


class SessionStorageActor(_impl_storage, _impl_add_item, _impl_remove_item, _impl_edit_item, _impl_remove_all__host):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/storage.js
    """


class ExtensionStorageActor(_impl_storage, _impl_remove_item, _impl_edit_item, _impl_remove_all__host):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/storage.js
    """


class CacheStorageActor(_impl_storage, _impl_remove_item, _impl_remove_all__host_name):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/storage.js
    """


class IndexedDBStorageActor(_impl_storage, _impl_remove_item):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/storage.js
    """

    def remove_database(self, host: str, name: str):
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "removeDatabase",
            "host": host,
            "name": name,
        })
