import esper
import math

from gamelib.ecs.geometry import PositionComponent, VelocityComponent
from gamelib.ecs.waypoint import WaypointComponent, WaypointProcessor


def test_waypoint_reaches_target_and_removes_component():
    proc = WaypointProcessor()

    ent = esper.create_entity()
    esper.add_component(ent, PositionComponent(0, 0))
    # velocity magnitude 100 px/s to the right
    esper.add_component(ent, VelocityComponent((100, 0)))
    esper.add_component(ent, WaypointComponent(waypoints=[(50, 0)], tolerance=1.0))

    # process with dt such that move_dist == 50 -> should arrive
    proc.process(0.5)

    pos = esper.component_for_entity(ent, PositionComponent)
    assert pos.x == 50
    assert pos.y == 0
    # waypoint component should be removed after arrival
    assert not esper.has_component(ent, WaypointComponent)


def test_velocity_vector_updated_toward_target():
    proc = WaypointProcessor()

    ent = esper.create_entity()
    esper.add_component(ent, PositionComponent(0, 0))
    # initial velocity set to magnitude 100 pointing right
    esper.add_component(ent, VelocityComponent((100, 0)))
    esper.add_component(
        ent, WaypointComponent(waypoints=[(0, 100)], tolerance=1.0, loop=True)
    )

    # run one small step
    proc.process(0.1)

    vel = esper.component_for_entity(ent, VelocityComponent)
    # velocity should now point roughly downward (0, positive)
    assert vel.base_speed[1] > 0
    # magnitude should remain approximately 100
    mag = math.hypot(vel.base_speed[0], vel.base_speed[1])
    assert abs(mag - 100) <= 1
