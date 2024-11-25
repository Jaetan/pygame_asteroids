"""Asteroid field."""

from __future__ import annotations
import random
from collections.abc import Callable
from typing import final, override, TYPE_CHECKING

from pygame.math import Vector2
from pygame.sprite import Sprite

from asteroid import Asteroid
from constants import (
    ASTEROID_KINDS,
    ASTEROID_MAX_RADIUS,
    ASTEROID_MIN_RADIUS,
    ASTEROID_SPAWN_RATE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)

if TYPE_CHECKING:
    from pygame.sprite import _Group  # pyright:ignore[reportPrivateUsage]


@final
class AsteroidField(Sprite):
    """Implementation of the asteroid field"""

    edges: list[tuple[Vector2, Callable[[float], Vector2]]] = [
        (
            Vector2(1, 0),
            lambda y: Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ),
        (
            Vector2(-1, 0),
            lambda y: Vector2(SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ),
        (
            Vector2(0, 1),
            lambda x: Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ),
        (
            Vector2(0, -1),
            lambda x: Vector2(x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS),
        ),
    ]

    def __init__(self, *asteroids_groups: _Group) -> None:
        super().__init__()
        self.spawn_timer = 0.0
        self.asteroids_groups = asteroids_groups

    def spawn(self, position: Vector2, radius: int, velocity: Vector2):
        """Spawn an asteroid"""
        _ = Asteroid(position, radius, velocity, *self.asteroids_groups)

    @override
    def update[**p](self, dt: float, /, *args: p.args, **kwargs: p.kwargs):
        """Update the field by spawning asteroids regularly"""
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(position, ASTEROID_MIN_RADIUS * kind, velocity)
