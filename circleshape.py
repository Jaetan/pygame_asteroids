"""Base class for all sprites in the game. Every sprite has a circular hitbox,
   which is an instance of this class."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from pygame.math import Vector2
from pygame.sprite import Group, Sprite
from pygame.surface import Surface

if TYPE_CHECKING:
    from pygame.sprite import _Group  # pyright:ignore[reportPrivateUsage]


class CircleShape(Sprite):
    """Base class for all sprites in the game."""

    def __init__(self, x: float, y: float, radius: int):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.position: Vector2 = Vector2(x, y)
        self.velocity: Vector2 = Vector2(0, 0)
        self.radius: int = radius

    def draw(self, _screen: Surface):
        """Draw a circular sprite on the given screen."""

    # dt is the first argument in *args
    @override
    def update[**p](self, *args: p.args, **kwargs: p.kwargs):
        """Update the state of the sprite (make it go forward)."""

    def collides_with(self, other: CircleShape) -> bool:
        """Check if this sprite collides with the specified other."""
        return self.position.distance_to(other.position) <= self.radius + other.radius
