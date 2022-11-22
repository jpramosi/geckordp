import os
import signal
import subprocess
import time
from pathlib import Path
from socket import socket
from sys import platform
from time import sleep
from typing import List
import psutil
from geckordp.logger import exlog, dlog


class ExpireAt():

    def __init__(self, sec: float):
        self.__start = time.time()
        self.__sec = sec

    def __bool__(self):
        return self.expired_time() < self.__sec

    def expired_time(self):
        return (time.time() - self.__start)

    def expired(self):
        return not self.__bool__()


def wait_process_loaded(pid: int, timeout_sec=15.0, check_sec=0.3, no_activity_threshold=9.0, no_activity_min_count=6) -> bool:
    """ Waits for a process til cpu activity settles down.

    Args:
        pid (int): The process ID.
        timeout_sec (float, optional): Maximum wait time. Defaults to 15.0.
        check_sec (float, optional): Interval between the measurements. Defaults to 0.3.
        no_activity_threshold (float, optional): The percentage threshold which sets the activity as low. Defaults to 9.0.
        no_activity_min_count (int, optional): The minimum amount to break on low activity. Defaults to 6.

    Returns:
        bool: True: if successful waited, False: failed to wait for process.
    """
    em = f"waiting for process[{pid}] failed"
    try:
        low_activity_in_row = 0
        proc_info = psutil.Process(pid)
        if (not proc_info):
            return False

        exp = ExpireAt(timeout_sec)
        while exp:
            cpu = proc_info.cpu_percent(check_sec)
            if (cpu < no_activity_threshold):
                low_activity_in_row += 1
            else:
                low_activity_in_row = 0
            if (low_activity_in_row >= no_activity_min_count):
                break

        dlog(f"expired={exp.expired()}")
        return not exp.expired()
    except psutil.NoSuchProcess:
        exlog(f"{em}, process no longer exists")
        return False
    except Exception as ex:
        exlog(f"{em}, wait 15 seconds:\n{ex}")
        sleep(15)
        return True


def wait_dir_changed(path: Path, timeout_sec=20.0, check_sec=0.3, min_file_age_sec=8.0, ignore_files: list | None = None) -> bool:
    """ Waits for the latest file modification in a path to reach a specified age in seconds.

    Args:
        path (Path): The input path to check for file modifications.
        timeout_sec (float, optional): Maximum wait time. Defaults to 20.0.
        check_sec (float, optional): Interval between the probes. Defaults to 0.3.
        min_file_age_sec (float, optional): Minimum file age. Defaults to 8.0.
        ignore_files (list, optional): Ignore a file if it contains a keyword in this list. Defaults to None.

    Raises:
        ValueError: If 'min_file_age_sec' is greater or equal than 'timeout_sec'.

    Returns:
        bool: True: if successful waited, False: on timeout.
    """
    if min_file_age_sec >= timeout_sec:
        raise ValueError()

    exp = ExpireAt(timeout_sec)
    if ignore_files is None:
        ignore_files = []

    while exp:

        latest_modification = 9999999999.0
        latest_file = ""
        for rootpath, _folders, files in os.walk(str(path)):
            for file in files:

                skip = False
                for ign_file in ignore_files:
                    if ign_file in file:
                        skip = True
                        break
                if skip:
                    continue

                try:
                    filepath = Path(rootpath).joinpath(file)
                    age = time.time() - os.stat(filepath).st_mtime
                    if age < latest_modification:
                        latest_modification = age
                        latest_file = file
                except:
                    pass

        if latest_modification > min_file_age_sec and latest_file != "":
            return True
        sleep(check_sec)
    return False


def kill(proc: subprocess.Popen) -> bool:
    """ Kill a process by handle.

    Args:
        proc (subprocess.Popen): The process handle.

    Returns:
        bool: True: if successful terminated, False: failed to terminate process.
    """
    try:
        success = True
        if platform == "win32":
            proc = subprocess.Popen(
                ["taskkill", "/F", "/T", "/PID",
                 str(proc.pid)],
                shell=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)
            success = proc.wait(5) == 0
        else:
            proc.send_signal(signal.SIGTERM)
        return success
    except Exception as ex:
        exlog(ex)
        return False


def kill_by_pid(pid: int) -> bool:
    """ Kill a process by handle.

    Args:
        pid (int): The process ID.

    Returns:
        bool: True: if successful terminated, False: failed to terminate process.
    """
    try:
        success = True
        if platform == "win32":
            proc = subprocess.Popen(
                ["taskkill", "/F", "/T", "/PID",
                 str(pid)],
                shell=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT)
            success = proc.wait(5) == 0
        else:
            proc = psutil.Process(pid)
            proc.send_signal(signal.SIGTERM)
        return success
    except Exception as ex:
        exlog(ex)
        return False


def find_free_ports(n=1) -> List[int]:
    """ Searches for free ports to use.

        .. note::
            It can't be guaranteed that the returned ports stay free.
            However it is very unlikely it happens in real-world situations as long
            the operating system doesn't allocate and free ports all the time.

    Args:
        n (int, optional): The amount of free ports to search. Defaults to 1.

    Returns:
        List[int]: A list of free ports.
    """
    if (n <= 0):
        return []
    sockets = []
    ports = []
    for _ in range(0, n):
        s = socket()
        s.bind(('', 0))
        sockets.append(s)
        ports.append(s.getsockname()[1])
    return ports
