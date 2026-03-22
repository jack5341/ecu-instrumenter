# -*- coding: utf-8 -*-
from __future__ import division
# ECU Instrumenter
# app/ECUInstrumenter/ecu_dashboard.py
#
# INSTALL ON MIYOO (OnionOS):
#   opkg update && opkg install python3 python3-pygame
#   Copy app/ECUInstrumenter/ to /mnt/SDCARD/
#   ssh root@<miyoo-ip>
#   python3 /mnt/SDCARD/ECUInstrumenter/ecu_dashboard.py

import sys

import pygame

import config as C
from renderer import Renderer
from simulator import Simulator


def main():
    pygame.init()
    pygame.display.set_caption(C.APP_NAME)
    screen = pygame.display.set_mode((C.WIDTH, C.HEIGHT))
    clock = pygame.time.Clock()
    sim = Simulator()
    renderer = Renderer()

    running = True
    while running:
        dt = clock.tick(C.FPS) / 1000.0
        renderer.fps = clock.get_fps() or float(C.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False

        sim.update(dt)
        renderer.draw(screen, sim)
        pygame.display.flip()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
