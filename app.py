from modules.arm import Arm, Segment
from modules.simulator import Simulator


left_arm = Arm(
    axis_pos=(.0, 50 / 2),
    segments=(
        Segment(length=100.0),
        Segment(length=100.0)
    )
)

right_arm = Arm(
    axis_pos=(.0, -50 / 2),
    segments=(
        Segment(length=100.0),
        Segment(length=100.0)
    )
)


sim = Simulator(
    arms=(left_arm, right_arm),
    configuration={
        "geometry": {"width": 1000, "height": 700},
        "origin": (200, 350),
        "win pos": f"{0}+{0}",
        "bg": "gray",
        "title": "Robotic paint simulator"
    }, ui=True
)

sim.sinus()
