import pytest
from gamelib.ecs.geometry import PositionComponent, RectComponent


def test_position_component_basic():
    """Verify PositionComponent creation, mutation, equality, and usage.

    - Construct a PositionComponent and check initial values
    - Mutate x/y and check that mutation sticks
    - Verify dataclass equality semantics
    - Ensure RectComponent.rect reflects PositionComponent coordinates
    """
    pos = PositionComponent(1, 2)

    # Creation
    assert pos.x == 1
    assert pos.y == 2
    assert isinstance(pos.x, int) and isinstance(pos.y, int)

    # Mutation
    pos.x = 5
    pos.y = -3
    assert pos.x == 5
    assert pos.y == -3

    # Equality
    assert PositionComponent(5, -3) == pos
    assert PositionComponent(0, 0) != pos

    # Interaction with RectComponent (rect.topleft should match pos)
    rect_comp = RectComponent(pos=pos, width=10, height=20)
    rect = rect_comp.rect
    assert (rect.x, rect.y) == (pos.x, pos.y)
    assert rect.size == (10, 20)
