from abc import ABC


class Actor(ABC):

    def __init__(self, rdp_client, actor_id = ""):
        self.__client = rdp_client
        self.__actor_id = actor_id

    @property
    def actor_id(self):
        return self.__actor_id

    @actor_id.setter
    def actor_id(self, value):
        self.__actor_id = value

    @property
    def client(self):
        return self.__client

    def add_handler(self, event, handler):
        self.__client.add_handler(event, handler)

    def del_handler(self, event, handler):
        self.__client.del_handler(event, handler)
