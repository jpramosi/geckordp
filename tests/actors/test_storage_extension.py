# pylint: disable=unused-import
from concurrent.futures import Future
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.events import Events
from geckordp.actors.watcher import WatcherActor
from geckordp.actors.storage import ExtensionStorageActor
from geckordp.logger import log, logdict

""" todo: ExtensionStorageActor requires to inspect extension's page. However it seems it may not be possible
    to retrieve the actor id.
    If you encounter this issue and found the identifier of the actor,
    please open an issue here https://github.com/jpramosi/geckordp/issues/new.
"""
