# pylint: disable=unused-import
import pytest
import tests.helpers.constants as constants
from tests.helpers.utils import *
from geckordp.rdp_client import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.accessibility.accessibility import AccessibilityActor
from geckordp.actors.accessibility.simulator import SimulatorActor
from geckordp.actors.accessibility.parent_accessibility import ParentAccessibilityActor
from geckordp.logger import log, logdict


def init():
    cl = RDPClient(3)
    cl.connect(constants.REMOTE_HOST, constants.REMOTE_PORT)
    root = RootActor(cl)
    current_tab = root.current_tab()
    tab = TabActor(cl, current_tab["actor"])
    actor_ids = tab.get_target()
    root_ids = root.get_root()
    accessibility = AccessibilityActor(cl, actor_ids["accessibilityActor"])
    simulator_id = accessibility.get_simulator().get("actor", None)
    if (simulator_id is None):
        log("No simulator actor found, firefox is probably running in headless mode")
        return cl, None
    simulator = SimulatorActor(cl, simulator_id)
    accessibility.bootstrap()
    parent = ParentAccessibilityActor(
        cl, root_ids["parentAccessibilityActor"])
    parent.bootstrap()
    parent.enable()
    return cl, simulator


def test_simulate():
    cl = None
    try:
        cl, simulator = init()
        if (simulator is None):
            return
        val = simulator.simulate(SimulatorActor.Types.PROTANOPIA)
        assert val.get("value", None) is not None
        val = simulator.simulate(SimulatorActor.Types.NONE)
        assert val.get("value", None) is not None
    finally:
        cl.disconnect()
