# pylint: disable=unused-import
import pytest
import tests.helpers.constants as constants
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.preference import PreferenceActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    root_ids = root.get_root()
    preference = PreferenceActor(
        cl, root_ids["preferenceActor"])
    return cl, preference


def test_get_traits():
    cl = None
    try:
        cl, preference = init()
        val = preference.get_traits().get("traits", 0)
        assert val != 0
    finally:
        cl.disconnect()


def test_get_bool_pref():
    cl = None
    try:
        cl, preference = init()
        val = preference.get_bool_pref(
            "toolkit.tabbox.switchByScrolling").get("value", None)
        assert val == True or val == False
    finally:
        cl.disconnect()


def test_get_char_pref():
    cl = None
    try:
        cl, preference = init()
        val = preference.get_char_pref(
            "devtools.debugger.chrome-debugging-host").get("value", "")
        assert "localhost" in val
    finally:
        cl.disconnect()


def test_get_int_pref():
    cl = None
    try:
        cl, preference = init()
        val = preference.get_int_pref(
            "devtools.debugger.end-panel-size").get("value", 0)
        assert val > 0
    finally:
        cl.disconnect()


def test_get_all_prefs():
    cl = None
    try:
        cl, preference = init()
        val = preference.get_all_prefs("test")
        assert len(val) > 100
    finally:
        cl.disconnect()


def test_set_bool_pref():
    cl = None
    try:
        cl, preference = init()
        val = preference.set_bool_pref(
            "toolkit.tabbox.switchByScrolling", False)["from"]
        assert "preferenceActor" in val
    finally:
        cl.disconnect()


def test_set_char_pref():
    cl = None
    try:
        cl, preference = init()
        val = preference.set_char_pref(
            "devtools.debugger.chrome-debugging-host", "localhost")["from"]
        assert "preferenceActor" in val
    finally:
        cl.disconnect()


def test_set_int_pref():
    cl = None
    try:
        cl, preference = init()
        val = preference.set_int_pref(
            "devtools.debugger.end-panel-size", 300)["from"]
        assert "preferenceActor" in val
    finally:
        cl.disconnect()


def test_clear_user_pref():
    cl = None
    try:
        cl, preference = init()
        preference.clear_user_pref(
            "toolkit.tabbox.switchByScrolling")
        preference.clear_user_pref(
            "devtools.debugger.chrome-debugging-host")
        val = preference.clear_user_pref(
            "devtools.debugger.end-panel-size")["from"]
        assert "preferenceActor" in val
    finally:
        cl.disconnect()
