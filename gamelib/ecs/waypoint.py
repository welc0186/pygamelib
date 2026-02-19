from dataclasses import dataclass
from typing import Callable, List, Tuple, Optional
import math

import esper

from gamelib.ecs.geometry import PositionComponent, VelocityComponent


@dataclass
class WaypointComponent:
    waypoints: List[Tuple[int, int]]
    tolerance: float = 2.0  # pixels
    loop: bool = False
    current_index: int = 0
    on_finished: Optional[Callable[[int], None]] = None


class WaypointProcessor(esper.Processor):
    def process(self, dt: float) -> None:
        # dt is expected in seconds
        for entity, waypoint in esper.get_component(WaypointComponent):
            if not esper.has_component(entity, PositionComponent):
                continue
            if not esper.has_component(entity, VelocityComponent):
                # require a VelocityComponent to determine movement speed
                continue
            pos = esper.component_for_entity(entity, PositionComponent)
            vel = esper.component_for_entity(entity, VelocityComponent)
            if not waypoint.waypoints:
                # nothing to do
                continue

            # Clamp current_index
            if waypoint.current_index >= len(waypoint.waypoints):
                if waypoint.loop:
                    waypoint.current_index = 0
                else:
                    if waypoint.on_finished:
                        waypoint.on_finished(entity)
                    esper.remove_component(entity, WaypointComponent)
                    continue

            target = waypoint.waypoints[waypoint.current_index]
            dx = target[0] - pos.x
            dy = target[1] - pos.y
            dist = math.hypot(dx, dy)

            if dist <= waypoint.tolerance:
                # Arrived at waypoint
                waypoint.current_index += 1
                if waypoint.current_index >= len(waypoint.waypoints):
                    if waypoint.loop:
                        waypoint.current_index = 0
                    else:
                        if waypoint.on_finished:
                            waypoint.on_finished(entity)
                        esper.remove_component(entity, WaypointComponent)
                continue

            # Determine movement speed from VelocityComponent
            base_x, base_y = vel.base_speed
            speed_magnitude = math.hypot(base_x, base_y) * getattr(vel, "multiplier", 1)

            # Move toward target using the velocity magnitude (dt seconds)
            if dist > 0 and speed_magnitude > 0:
                nx = dx / dist
                ny = dy / dist
                move_dist = speed_magnitude * dt
                # update velocity vector to point toward the target
                vel.base_speed = (int(nx * speed_magnitude), int(ny * speed_magnitude))
                if move_dist >= dist:
                    pos.x = int(target[0])
                    pos.y = int(target[1])
                    waypoint.current_index += 1
                    # Check for completion after stepping to target
                    if waypoint.current_index >= len(waypoint.waypoints):
                        if waypoint.loop:
                            waypoint.current_index = 0
                        else:
                            if waypoint.on_finished:
                                waypoint.on_finished(entity)
                            esper.remove_component(entity, WaypointComponent)
                else:
                    pos.x = int(pos.x + nx * move_dist)
                    pos.y = int(pos.y + ny * move_dist)
