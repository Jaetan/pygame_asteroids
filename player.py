"""Player class for the game."""

from __future__ import annotations

from typing import TYPE_CHECKING, final, override

import pygame
from pygame.math import Vector2

from circleshape import CircleShape
from constants import (
    PLAYER_SHOOT_COOLDOWN,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
    SHOT_RADIUS,
)
from shot import Shot

if TYPE_CHECKING:
    from pygame.sprite import _Group  # pyright:ignore[reportPrivateUsage]


@final
class Player(CircleShape):
    """The circle shape around the player."""

    def __init__(
        self,
        position: Vector2,
        radius: int,
        velocity: Vector2,
        shots_groups: _Group,
        /,
        *groups: _Group,
    ) -> None:
        super().__init__(position, radius, velocity, *groups)
        self.rotation = 0
        self.shots_cooldown = 0
        self.shots_groups = (shots_groups,) + groups

    def triangle(self) -> list[Vector2]:
        """The triangle representing the player on the screen."""
        forward = Vector2(0, 1).rotate(self.rotation)
        right = Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        return [
            self.position + forward * self.radius,
            self.position - forward * self.radius - right,
            self.position - forward * self.radius + right,
        ]

    @override
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the player on the screen."""
        _ = pygame.draw.polygon(
            surface=screen, color="white", points=self.triangle(), width=2
        )

    def rotate(self, dt: float) -> None:
        """Rotate the player by the given angle."""
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt: float) -> None:
        """Move the player."""
        forward = Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self) -> None:
        """Shoot a bullet straight ahead."""
        if self.shots_cooldown == 0:
            velocity = Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            _ = Shot(Vector2(self.position), SHOT_RADIUS, velocity, *self.shots_groups)
            self.shots_cooldown = PLAYER_SHOOT_COOLDOWN

    @override
    def update[**p](self, dt: float, /, *args: p.args, **kwargs: p.kwargs):
        """Update the player."""
        self.shots_cooldown = max(self.shots_cooldown - dt, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
