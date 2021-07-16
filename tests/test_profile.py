# pylint: disable=unused-import
import os
import pytest
import tests.helpers.utils as utils
import tests.helpers.constants as constants
from geckordp.firefox import Firefox
from geckordp.profile import FirefoxProfile, ProfileManager
from geckordp.logger import log, logdict


PROFILES_PATH = Firefox.get_profiles_path()


def init():
    pm = ProfileManager()
    return pm


def test_create():
    pm = init()
    assert pm.create(constants.PROFILE0) == None
    assert pm.create(constants.PROFILE1) != None
    found = False
    for _currentpath, folders, _files in os.walk(str(PROFILES_PATH)):
        for folder in folders:
            if (constants.PROFILE1 in folder):
                found = True
                break
    assert found
    assert pm.remove(constants.PROFILE1)

    exception = False
    try:
        pm.create("")
    except ValueError:
        exception = True
    assert exception


def test_clone():
    pm = init()
    assert pm.clone(constants.PROFILE0, constants.PROFILE1) != None
    assert pm.clone(constants.PROFILE0, constants.PROFILE1) == None
    for _currentpath, folders, _files in os.walk(str(PROFILES_PATH)):
        for folder in folders:
            if (constants.PROFILE1 in folder):
                found = True
                break
    assert found
    assert pm.remove(constants.PROFILE1)

    exception = False
    try:
        pm.clone(constants.PROFILE0, constants.PROFILE0)
    except ValueError:
        exception = True
    assert exception

    exception = False
    try:
        pm.clone("", constants.PROFILE0)
    except ValueError:
        exception = True
    assert exception

    exception = False
    try:
        pm.clone(constants.PROFILE0, "")
    except ValueError:
        exception = True
    assert exception

    exception = False
    try:
        pm.clone("", "")
    except ValueError:
        exception = True
    assert exception


def test_remove():
    pm = init()
    assert not pm.remove(constants.PROFILE1)
    assert pm.create(constants.PROFILE1) != None
    assert pm.remove(constants.PROFILE1)
    assert not pm.exists(constants.PROFILE1)

    exception = False
    try:
        pm.remove("")
    except ValueError:
        exception = True
    assert exception


def test_list_profiles():
    pm = init()
    p1 = pm.create(constants.PROFILE1)
    p2 = pm.create(constants.PROFILE2)
    assert p1 != None
    assert p2 != None
    profiles = pm.list_profiles()
    for profile in profiles:
        if (profile == p1):
            p1 = None
        if (profile == p2):
            p2 = None
    assert p1 == None
    assert p2 == None
    assert pm.remove(constants.PROFILE1)
    assert pm.remove(constants.PROFILE2)


def test_exists():
    pm = init()
    assert pm.exists(constants.PROFILE0)
    assert not pm.exists(constants.PROFILE1)

    exception = False
    try:
        pm.exists("")
    except ValueError:
        exception = True
    assert exception


def test_get_profile_by_name():
    pm = init()
    assert pm.get_profile_by_name(constants.PROFILE0) != None
    assert pm.get_profile_by_name(constants.PROFILE1) == None

    exception = False
    try:
        pm.get_profile_by_name("")
    except ValueError:
        exception = True
    assert exception


def test_profile_config_set_get():
    pm = init()

    p0 = pm.clone(constants.PROFILE0, constants.PROFILE1)
    assert p0 != None

    p0.set_config("devtools.chrome.enabled", False)
    assert not p0.get_config("devtools.chrome.enabled")

    p0.set_required_configs()
    assert p0.get_config("devtools.chrome.enabled")

    p0.set_config("devtools.chrome.enabled", False)
    assert not p0.get_config("devtools.chrome.enabled")

    assert pm.remove(constants.PROFILE1)


def test_profile_remove_config():
    pm = init()

    p0 = pm.clone(constants.PROFILE0, constants.PROFILE1)
    assert p0 != None

    assert p0.get_config("devtools.chrome.enabled") != None
    p0.remove_config("devtools.chrome.enabled")
    assert p0.get_config("devtools.chrome.enabled") == None

    assert pm.remove(constants.PROFILE1)
