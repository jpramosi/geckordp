from enum import Enum
from geckordp.actors.actor import Actor


class SimulatorActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/accessibility.js#L212
    """

    class Types(str, Enum):
        NONE = "NONE"
        PROTANOPIA = "PROTANOPIA"
        DEUTERANOPIA = "DEUTERANOPIA"
        TRITANOPIA = "TRITANOPIA"
        ACHROMATOPSIA = "ACHROMATOPSIA"
        CONTRAST_LOSS = "CONTRAST_LOSS"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def simulate(self, simulate_matrix: Types = Types.NONE):
        args = []
        if (simulate_matrix != SimulatorActor.Types.NONE):
            args.append(simulate_matrix.value)
        return self.client.send_receive({
            "to": self.actor_id,
            "type": "simulate",
            "options": {
                "types": args,
            },
        })
