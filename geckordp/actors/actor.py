from abc import ABC
from geckordp.rdp_client import RDPClient


class Actor(ABC):

    def __init__(self, rdp_client: RDPClient, actor_id=""):
        self.__client = rdp_client
        self.__actor_id = actor_id

    @property
    def actor_id(self):
        return self.__actor_id

    @actor_id.setter
    def actor_id(self, value: str):
        self.__actor_id = value

    @property
    def client(self):
        return self.__client
