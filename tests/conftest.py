# pylint: disable=unused-import,wrong-import-position
from subprocess import Popen
import sys
import os
import logging
from functools import partial
import pytest
from geckordp.logger import log, wlog, set_stdout_log_level
from geckordp.settings import GECKORDP
from geckordp.profile import ProfileManager
from geckordp.firefox import Firefox
from geckordp.utils import kill
sys.path.append(os.path.join(os.path.dirname(__file__), 'helpers'))
from tests.helpers.utils import is_port_open
import tests.helpers.constants as constants


def dispose(pm: ProfileManager, handle: Popen):
    log(f"tests finished")
    if (handle is not None):
        kill(handle)
        pm.remove(constants.PROFILE0)
        pm.remove(constants.PROFILE1)
        pm.remove(constants.PROFILE2)
        try:
            handle.wait(5.0)
        except:
            pass


@pytest.fixture(scope="session", autouse=True)
def initialize(request):
    pm = ProfileManager()
    handle = None

    capmanager = request.config.pluginmanager.getplugin("capturemanager")
    with capmanager.global_and_fixture_disabled():
        # set debug parameters
        set_stdout_log_level(logging.DEBUG)
        GECKORDP.DEBUG_REQUEST = 1
        GECKORDP.DEBUG_RESPONSE = 1

        # start firefox if port is open
        if (not is_port_open(constants.REMOTE_HOST, constants.REMOTE_PORT)):
            pm.remove(constants.PROFILE0)
            pm.remove(constants.PROFILE1)
            pm.remove(constants.PROFILE2)
            log(f"initialize profile '{constants.PROFILE0}'")
            # create and modify profile
            profile = pm.create(constants.PROFILE0)
            profile.set_required_configs()

            # start firefox with subprocess
            log(
                f"start firefox with debug server on localhost:{constants.REMOTE_PORT}")
            handle = Firefox.start("https://example.com/",
                                   port=constants.REMOTE_PORT,
                                   profile=constants.PROFILE0,
                                   append_args=["-headless"],
                                   auto_kill=False)

        else:
            # firefox can also be started and kept open with:
            # firefox -new-instance -no-remote -new-window https://example.com/ -p geckordp --start-debugger-server 6000
            wlog(f"{constants.REMOTE_HOST}{constants.REMOTE_PORT} already in use")

        request.addfinalizer(
            partial(dispose, pm, handle))  # type: ignore
