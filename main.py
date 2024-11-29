"""Ateroids game."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import pygame
from pygame.base import init
from pygame.display import set_mode
from pygame.sprite import Group
from pygame.time import Clock

from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from player import Player

if TYPE_CHECKING:
    from pygame.sprite import _Group  # pyright:ignore[reportPrivateUsage]


def main():
    """Run the game."""
    _ = init()
    screen = set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = Clock()

    updatable: _Group = Group()
    drawable: _Group = Group()
    asteroids: _Group = Group()
    shots: _Group = pygame.sprite.Group()

    _ = AsteroidField(updatable, asteroids, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, shots, updatable, drawable)
    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        for obj in updatable:
            obj.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                print("Game over!")
                sys.exit()

            for shot in shots:
                if asteroid.collides_with(shot):
                    shot.kill()
                    asteroid.split()

        _ = screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
