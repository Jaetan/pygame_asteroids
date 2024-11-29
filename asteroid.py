"""Implementation of the asteroid sprite."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, cast, final, override

from pygame.draw import circle
from pygame.math import Vector2
from pygame.surface import Surface

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS

if TYPE_CHECKING:
    from pygame.sprite import _Group  # pyright:ignore[reportPrivateUsage]


@final
class Asteroid(CircleShape):
    """The asteroid sprite."""

    def __init__(
        self, x: float, y: float, radius: int, velocity: Vector2, *groups: _Group
    ):
        super().__init__(x, y, radius, velocity, *groups)
        self.asteroid_groups = groups

    @override
    def draw(self, screen: Surface):
        _ = circle(screen, "white", self.position, self.radius, 2)

    @override
    def update[**p](self, *args: p.args, **kwargs: p.kwargs):
        dt = cast(int, args[0])
        self.position += self.velocity * dt

    def split(self):
        """Split an asteroid in two if big enough. Otherwise, kill it."""
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        # randomize the angle of the split
        random_angle = random.uniform(20, 50)

        a = self.velocity.rotate(random_angle)
        b = self.velocity.rotate(-random_angle)

        new_radius: int = self.radius - ASTEROID_MIN_RADIUS
        _ = Asteroid(
            self.position.x, self.position.y, new_radius, a * 1.2, *self.asteroid_groups
        )
        _ = Asteroid(
            self.position.x, self.position.y, new_radius, b * 1.2, *self.asteroid_groups
        )
