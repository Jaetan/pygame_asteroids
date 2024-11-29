"""The player in the game, with his startship. The starship has a circular hitbox."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast, final, override

from pygame import Surface, Vector2
from pygame.constants import K_SPACE, K_a, K_d, K_s, K_w
from pygame.draw import polygon
from pygame.key import get_pressed

from circleshape import CircleShape
from constants import (
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
)
from shot import Shot

if TYPE_CHECKING:
    from pygame.sprite import _Group  # pyright:ignore[reportPrivateUsage]


@final
class Player(CircleShape):
    """The player in the game."""

    def __init__(self, x: float, y: float, velocity: Vector2, *groups: _Group):
        self.shots_group, *self.player_groups = groups
        super().__init__(x, y, PLAYER_RADIUS, velocity, *self.player_groups)
        self.rotation = 0
        self.shoot_timer: float = 0

    @override
    def draw(self, screen: Surface):
        _ = polygon(screen, "white", self.triangle(), 2)

    def triangle(self) -> list[Vector2]:
        """Returns the vertices of the triangle representing the player's spaceship."""
        forward = Vector2(0, 1).rotate(self.rotation)
        right = Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    @override
    def update[**p](self, *args: p.args, **kwargs: p.kwargs):
        dt = cast(int, args[0])
        self.shoot_timer -= dt
        keys = get_pressed()

        if keys[K_w]:
            self.move(dt)
        if keys[K_s]:
            self.move(-dt)
        if keys[K_a]:
            self.rotate(-dt)
        if keys[K_d]:
            self.rotate(dt)
        if keys[K_SPACE]:
            self.shoot()

    def shoot(self):
        """Shoot a bullet."""
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        velocity = Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        _ = Shot(
            self.position.x,
            self.position.y,
            velocity,
            self.shots_group,
            *self.player_groups,
        )

    def rotate(self, dt: int):
        """Rotate the player's spaceship clockwise, given the specified time span
        and internal angular velocity of the ship."""
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt: int):
        """Move the spaceship forward, given the specified time span and the internal
        spaceship speed."""
        forward = Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
