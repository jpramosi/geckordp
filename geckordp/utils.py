import time
import subprocess
import signal
from sys import platform
from typing import List
from socket import socket
import psutil
from geckordp.logger import exlog


class ExpireAt():

    def __init__(self, sec: int):
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
        bool: 
    """
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

    return not exp.expired()


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
