"""Shots fired by the player."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast, final, override

from pygame import Surface
from pygame.draw import circle

from circleshape import CircleShape
from constants import SHOT_RADIUS

if TYPE_CHECKING:
    from pygame.sprite import _Group  # pyright:ignore[reportPrivateUsage]


@final
class Shot(CircleShape):
    """A shot fired by the player."""

    def __init__(self, x: float, y: float, *groups: _Group):
        super().__init__(x, y, SHOT_RADIUS, *groups)

    @override
    def draw(self, screen: Surface):
        _ = circle(screen, "white", self.position, self.radius, 2)

    @override
    def update[**p](self, *args: p.args, **kwargs: p.kwargs):
        dt = cast(int, args[0])
        self.position += self.velocity * dt
