# pylint: disable=unused-import
import sys
import os
import logging
import subprocess
import atexit
from time import sleep
from geckordp.logger import init_logger, set_file_logger, log, elog, wlog, set_stdout_log_level
from geckordp.settings import GECKORDP
from geckordp.profile import FirefoxProfile, ProfileManager
from geckordp.firefox import Firefox
from geckordp.utils import kill
from tests.helpers.utils import is_port_open
import tests.helpers.constants as constants
sys.path.append(os.path.join(os.path.dirname(__file__), 'helpers'))


def start_tests():

    # run tests in subprocess in order to get the output
    # from pytest and geckordp (messing up with logging handlers didn't work well)
    log_file = "test.log"
    with open(log_file, "w") as f:
        # if subprocess, execute tests
        if ("-s" in sys.argv):

            # set debug parameters
            set_stdout_log_level(logging.DEBUG)
            GECKORDP.DEBUG_REQUEST = 1
            GECKORDP.DEBUG_RESPONSE = 1

            # start firefox if port is open
            if (not is_port_open(constants.REMOTE_HOST, constants.REMOTE_PORT)):
                # clone and modify default profile
                profile_name = "geckordp"
                log(f"initialize profile '{profile_name}'")
                pm = ProfileManager()
                pm.clone("default-release", profile_name)
                profile = pm.get_profile_by_name(profile_name)
                profile.set_required_configs()

                # start firefox with subprocess
                log(f"start firefox with debug server on localhost:{constants.REMOTE_PORT}")
                Firefox.start("https://example.com/",
                              constants.REMOTE_PORT,
                              profile_name,
                              ["-headless"])
            else:
                # firefox can also be started and kept open with:
                # firefox -new-instance -no-remote -new-window http://example.com/ -p geckordp --start-debugger-server 6000
                wlog(f"{constants.REMOTE_HOST}{constants.REMOTE_PORT} already in use")
            return
        
        # start subprocess
        sys.argv.append("-s")
        p = subprocess.Popen(sys.argv, stdout=f, stderr=f)
        p.wait(380)
        print(f"tests finished, logs can be obtained at '{log_file}'")
        
    sys.exit(0)

start_tests()
