"""The field of asteroids, spawning asteroids at the border of the screen."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, Callable, cast, final, override

from pygame import Vector2
from pygame.sprite import Group, Sprite

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
    """Asteroid's field, controlling the spawning of asteroids."""

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

    def __init__(self, *groups: _Group):
        self.updatable, *self.asteroids_groups = groups
        super().__init__(self.updatable)
        self.spawn_timer = 0.0

    def spawn(self, radius: int, position: Vector2, velocity: Vector2):
        """Spawn a new asteroid in the field."""
        _ = Asteroid(
            position.x,
            position.y,
            radius,
            velocity,
            self.updatable,
            self.asteroids_groups,
        )

    @override
    def update[**p](self, *args: p.args, **kwargs: p.kwargs):
        dt = cast(int, args[0])
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
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
