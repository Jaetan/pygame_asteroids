"""CircleShape is used as the base shape for all sprites in the game."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Sprite
from pygame.surface import Surface

if TYPE_CHECKING:
    from pygame.sprite import _Group  # pyright:ignore[reportPrivateUsage]


class CircleShape(Sprite):
    """Sprite implementation in the game: a circle with specified radius and center."""

    def __init__(
        self, position: Vector2, radius: int, velocity: Vector2, *groups: _Group
    ) -> None:
        super().__init__(*groups)
        self.position: Vector2 = position
        self.radius: int = radius
        self.velocity: Vector2 = velocity
        self.image: Surface = Surface((2 * radius, 2 * radius))
        _ = self.image.fill((0, 0, 0))
        self.rect: Rect = self.image.get_rect(center=position)

    def draw(self, _screen: Surface) -> None:
        """Draw the sprite on the screen (must be overriden by sub-classes)"""

    @override
    def update[**p](self, dt: float, /, *args: p.args, **kwargs: p.kwargs) -> None:
        """Update the state of the sprite (must be overriden by sub-classes)"""

    def collides_with(self, other: CircleShape) -> bool:
        """Return True if this sprite collides with the specified other"""
        return self.position.distance_to(other.position) <= self.radius + other.radius
