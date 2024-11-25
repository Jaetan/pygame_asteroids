"""Implementation of the asteroids."""

from typing import TypeVar, final, override

import pygame
from pygame.surface import Surface

from circleshape import CircleShape

K = TypeVar("K")


@final
class Asteroid(CircleShape):
    """Asteroid class."""

    @override
    def update[**p](self, dt: float, /, *args: p.args, **kwargs: p.kwargs):
        """Update the asteroid."""
        self.position += self.velocity * dt

    @override
    def draw(self, screen: Surface):
        """Draw the asteroid."""
        _ = pygame.draw.circle(
            surface=screen,
            color=(255, 255, 255),
            center=self.position,
            radius=self.radius,
            width=1,
        )
