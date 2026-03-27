# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from __future__ import division
import sys
import pygame

from config import settings as C
from core.state import global_state, AppScreen
from ui.fonts import UIFonts
from ui.screens.connection import ConnectionScreen
from ui.screens.dashboard import DashboardScreen
from ui.screens.logs import LogScreen
from ui.screens.settings import SettingsScreen
from ui.screens.loading import LoadingScreen
from ui.screens.errors import ErrorsScreen

def main():
    pygame.init()
    pygame.display.set_caption(C.APP_NAME)
    screen = pygame.display.set_mode((C.WIDTH, C.HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
    clock = pygame.time.Clock()

    fonts = UIFonts.create()
    
    global_state.load()

    screens = {
        AppScreen.CONNECTION: ConnectionScreen(fonts),
        AppScreen.LOADING: LoadingScreen(fonts),
        AppScreen.DASHBOARD: DashboardScreen(fonts),
        AppScreen.LOG: LogScreen(fonts),
        AppScreen.ERRORS: ErrorsScreen(fonts),
        AppScreen.SETTINGS: SettingsScreen(fonts),
    }

    running = True
    while running:
        dt = clock.tick(C.FPS) / 1000.0
        fps = clock.get_fps() or float(C.FPS)

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                running = False
            screens[global_state.screen].handle_event(event)

        # Draw current screen
        active_screen = screens[global_state.screen]
        if global_state.screen == AppScreen.DASHBOARD:
            active_screen.update(dt)
            active_screen.draw(screen, fps)
        elif global_state.screen == AppScreen.LOADING:
            active_screen.update(dt)
            active_screen.draw(screen)
        else:
            active_screen.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    main()
