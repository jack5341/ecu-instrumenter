from __future__ import annotations

import sys

import pygame

from config import settings as C
from sim.simulator import Simulator
from ui.renderer import Renderer


def main() -> None:
    pygame.init()
    pygame.display.set_caption(C.APP_NAME)
    screen = pygame.display.set_mode((C.WIDTH, C.HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
    clock = pygame.time.Clock()

    simulator = Simulator()
    renderer = Renderer()

    running = True
    while running:
        dt = clock.tick(C.FPS) / 1000.0
        renderer.fps = clock.get_fps() or float(C.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q):
                running = False

        frame = simulator.update(dt)
        renderer.draw(screen, frame)
        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
