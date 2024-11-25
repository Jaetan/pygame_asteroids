"""Main module for the asteroids game."""

from __future__ import annotations
from typing import TYPE_CHECKING, cast
import pygame
from pygame.math import Vector2
from pygame.sprite import Group

from asteroidfield import AsteroidField
from circleshape import CircleShape
from constants import PLAYER_RADIUS, SCREEN_HEIGHT, SCREEN_WIDTH
from player import Player

if TYPE_CHECKING:
    from pygame.sprite import _Group  # pyright:ignore[reportPrivateUsage]


def main() -> None:
    """Main function for the asteroids game."""

    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    _ = pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    updatables: _Group = Group()
    drawables: _Group = Group()
    asteroids: _Group = Group()

    player = Player(
        Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
        PLAYER_RADIUS,
        Vector2(0, 0),
        updatables,
        drawables,
    )
    field = AsteroidField(asteroids, updatables, drawables)
    field.add(updatables)

    clock = pygame.time.Clock()
    dt = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Something is wrong with how sprites are grouped and drawn: we shouldn't
        # have to cast everything to a CircleShape, and we shouldn't have to clear
        # the screen at each step. Investigate.
        _ = screen.fill((0, 0, 0))
        updatables.update(dt)
        for drawable in drawables:
            cast(CircleShape, cast(object, drawable)).draw(screen)
        for asteroid in asteroids:
            if player.collides_with(cast(CircleShape, cast(object, asteroid))):
                print("Game over!")
                running = False

        pygame.display.flip()
        dt = clock.tick(60) / 1000
    pygame.quit()


if __name__ == "__main__":
    main()
