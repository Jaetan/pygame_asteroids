"""Implementation of a shot (bullet)."""

from typing import final, override

from pygame import Surface
import pygame

from circleshape import CircleShape
from constants import SHOT_RADIUS

@final
class Shot(CircleShape):
    """Bullets fired at asteroids."""

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
            radius=SHOT_RADIUS,
            width=1,
        )
