import string
import subprocess
import atexit
from threading import Lock
from typing import List
from os import path as ospath
from sys import platform
from pathlib import Path
from geckordp.utils import kill_by_pid, wait_process_loaded

_MTX = Lock()
_REGISTERED = False
_PIDS = []

def _kill_instances():
    with _MTX:
        for pid in _PIDS:
            kill_by_pid(pid)

class Firefox():

    @staticmethod
    def get_profiles_path() -> Path:
        """ Get the path of firefox profiles.

        Raises:
            RuntimeError: If platform is not supported.

        Returns:
            Path: The path of firefox profiles.
        """
        if "linux" in platform:
            return Path.home().joinpath(".mozilla/firefox/")
        elif platform == "darwin":
            return Path.home().joinpath("Library/Application Support/Firefox/")
        elif platform == "win32":
            return Path(ospath.expandvars(r"%APPDATA%\\Mozilla\\Firefox\\"))
        else:
            raise RuntimeError(f"The platform '{platform}' is not supported")

    @staticmethod
    def get_binary_path() -> str:
        """ Get the path of the firefox binary.

        Raises:
            RuntimeError: If platform is not supported.
            RuntimeError: If firefox is not found.

        Returns:
            Path: The path of firefox profiles.
        """
        if "linux" in platform:
            return "firefox"
        elif platform == "darwin":
            return "firefox"
        elif platform == "win32":
            drives = [Path(f"{x}:") for x in string.ascii_uppercase if Path(f"{x}:").exists()]
            paths = []
            for d in drives:
                p = d.joinpath("\\Program Files\\Mozilla Firefox\\firefox.exe")
                if (not p.exists()):
                    paths.append(p)
                    continue
                return str(p)
            raise RuntimeError(f"Could not find firefox binary for '{platform}' in:\n{paths}")
        else:
            raise RuntimeError(f"The platform '{platform}' is not supported")

    @staticmethod
    def start(url: str, port: int, profile: str, append_args: List[str] = None) -> subprocess.Popen:
        """ Starts a firefox instance.

            .. note:: 
                The profile needs to be once configured with :func:`~geckordp.profile.FirefoxProfile.set_required_configs`.
                To manually start firefox, this command can be used:

                **firefox -new-instance -no-remote -new-window http://example.com/ -p geckordp --start-debugger-server 6000**

        Args:
            url (str): The url for the start page
            port (int): The port to use for the rdp server.
            profile (str): The profile to use.
            append_args (List[str], optional): Additional args for Firefox. Defaults to None.

        Returns:
            subprocess.Popen: The process handle.
        """
        args = [Firefox.get_binary_path(),
                "-new-instance",
                "-no-remote",
                "-no-default-browser-check",
                "-new-window", url,
                "-p", profile,
                "--start-debugger-server", str(port)
                ]
        for arg in append_args:
            args.append(arg)
        proc = subprocess.Popen(args, shell=False)
        wait_process_loaded(proc.pid)
        
        global _MTX
        global _REGISTERED
        global _PIDS
        with _MTX:
            _PIDS.append(proc.pid)
            if (not _REGISTERED):
                _REGISTERED = True
                atexit.register(_kill_instances)
        return proc
